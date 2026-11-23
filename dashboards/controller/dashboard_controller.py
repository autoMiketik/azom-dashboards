#!/usr/bin/env python3
"""Switch AZOM wheel dashboards when supported SimHub settings change."""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import math
import time
from pathlib import Path
from typing import Any

LOG = logging.getLogger("moza-dashboard-controller")


class PropertyFeed:
    """Subscribe to SimHub properties through SimHub Property Server."""

    def __init__(self, host: str, port: int, properties: list[str],
                 queue: asyncio.Queue[tuple[str, Any]]) -> None:
        self.host = host
        self.port = port
        self.properties = properties
        self.queue = queue

    async def run(self) -> None:
        """Reconnect and publish property updates until the program exits."""
        while True:
            writer = None
            try:
                reader, writer = await asyncio.open_connection(self.host, self.port)
                self.queue.put_nowait(("__feed_connected__", True))
                greeting = await reader.readline()
                LOG.info("Connected to %s:%d (%s)", self.host, self.port,
                         greeting.decode(errors="replace").strip())
                for name in self.properties:
                    writer.write(f"subscribe {name}\n".encode())
                await writer.drain()
                while line := await reader.readline():
                    message = line.decode(errors="replace").rstrip("\r\n")
                    if message.startswith("Property "):
                        parts = message.split(" ", 3)
                        if len(parts) == 4:
                            _prefix, name, _kind, value = parts
                            self.queue.put_nowait((name, self._value(value)))
                    elif message.startswith("ERROR"):
                        LOG.warning("Property Server: %s", message)
            except (OSError, asyncio.IncompleteReadError) as exc:
                LOG.warning("Property Server unavailable: %s", exc)
            finally:
                self.queue.put_nowait(("__feed_connected__", False))
                if writer is not None:
                    writer.close()
                    try:
                        await writer.wait_closed()
                    except OSError:
                        pass
            await asyncio.sleep(2)

    @staticmethod
    def _value(raw: str) -> Any:
        if raw == "(null)":
            return None
        if raw in ("True", "False"):
            return raw == "True"
        try:
            number = float(raw)
        except ValueError:
            return raw
        return int(number) if number.is_integer() else number


class DashboardController:
    """Detect setting changes and navigate through the configured wheel slots."""

    def __init__(self, config: dict[str, Any], queue: asyncio.Queue) -> None:
        self.config = config
        self.queue = queue
        self.values: dict[str, Any] = {}
        self.order = config["dashboard_order"]
        self.mains = config["main_dashboards"]
        self.main_indices = {self.order.index(name) for name in self.mains}
        self.settings = config["settings"]
        self.setting_by_property = {item["property"]: (index, item)
                                    for index, item in enumerate(self.settings)}
        self.active_page: str | None = None
        self.last_main: str | None = None
        self.return_page: str | None = None
        self.in_popup_sequence = False
        self.deadline: float | None = None
        self.pending_changes: list[tuple[float, int, dict[str, Any]]] = []
        self.baselines: dict[str, float | None] = {
            item["property"]: None for item in self.settings
        }
        self.feed_connected = False
        self.wheel_connected = False
        self.game_running = False
        self.expected_page: str | None = None
        self.page_revision = 0
        self.page_event = asyncio.Event()
        self.desired_page: str | None = None
        self.navigator: asyncio.Task | None = None

    @property
    def page_property(self) -> str:
        return self.config["properties"]["dashboard"]

    def required_properties(self) -> list[str]:
        names = list(self.config["properties"].values())
        names.extend(item["property"] for item in self.settings)
        return list(dict.fromkeys(names))

    async def handle(self, name: str, value: Any) -> None:
        if name == "__feed_connected__":
            self.feed_connected = bool(value)
            self._clear_baselines()
            if not self.feed_connected:
                self._cancel_sequence()
                self.expected_page = None
                LOG.info("Property feed disconnected; popup detection paused")
            else:
                LOG.info("Property feed connected")
            return

        old = self.values.get(name, _MISSING)
        self.values[name] = value

        if name == self.page_property:
            self._handle_page(value)
        elif name == self.config["properties"]["wheel_connected"]:
            self._handle_wheel_connected(value)
        elif name == self.config["properties"]["session_restart"]:
            if self._as_bool(value) is True:
                self._reset_for_context("session restart")
        elif name in (self.config["properties"]["game_running"],
                      self.config["properties"]["game"],
                      self.config["properties"]["car"],
                      self.config["properties"]["track"],
                      self.config["properties"]["session"]):
            self._handle_context(name, old, value)
        elif name in self.setting_by_property:
            self._handle_setting(name, value)

    def _handle_page(self, value: Any) -> None:
        if not isinstance(value, str) or value not in self.order:
            if value is not None:
                LOG.warning("Active dashboard %r is not in dashboard_order; update controller.json", value)
            return
        previous = self.active_page
        if previous == value:
            return
        self.active_page = value
        self.page_revision += 1
        self.page_event.set()
        LOG.info("Dashboard: %s", value)

        if self.expected_page is not None:
            expected = self.expected_page
            self.expected_page = None
            if value == expected:
                if value in self.mains:
                    self.last_main = value
                return
            LOG.info("Dashboard changed to %s during navigation to %s; treating as manual selection",
                     value, expected)
            self._manual_page_change(previous, value)
            return
        self._manual_page_change(previous, value)

    def _manual_page_change(self, previous: str | None, current: str) -> None:
        if current in self.mains:
            self.last_main = current
            if self.in_popup_sequence:
                LOG.info("Manual main-page selection cancels popup sequence")
                self._cancel_sequence()
                self.desired_page = None
            return

        if self.in_popup_sequence:
            LOG.info("Manual popup-page change cancels the active sequence")
            self._cancel_sequence()
        target = self._main_after_manual_popup(previous, current)
        if target:
            LOG.info("Skipping popup slot during normal page navigation; returning to %s", target)
            self.desired_page = target
            self._start_navigator()

    def _main_after_manual_popup(self, previous: str | None, current: str) -> str | None:
        current_index = self.order.index(current)
        if previous in self.mains:
            previous_index = self.order.index(previous)
            if current_index == (previous_index + 1) % len(self.order):
                direction = 1
            elif current_index == (previous_index - 1) % len(self.order):
                direction = -1
            else:
                direction = 1
            start = previous_index
        else:
            direction = 1
            start = current_index
        for step in range(1, len(self.order) + 1):
            candidate = self.order[(start + direction * step) % len(self.order)]
            if candidate in self.mains:
                return candidate
        return None

    def _handle_wheel_connected(self, value: Any) -> None:
        connected = self._as_bool(value)
        if connected is None or connected == self.wheel_connected:
            return
        self.wheel_connected = connected
        self._clear_baselines()
        if not connected:
            LOG.info("Wheel disconnected; popup state reset")
            self._cancel_sequence()
            self.desired_page = None
        elif self.active_page and self.active_page not in self.mains:
            target = self._main_after_manual_popup(None, self.active_page)
            self.desired_page = target
            self._start_navigator()
        else:
            self.last_main = self.active_page if self.active_page in self.mains else None

    def _handle_context(self, name: str, old: Any, value: Any) -> None:
        if name == self.config["properties"]["game_running"]:
            running = self._as_bool(value)
            if running is not None and running != self.game_running:
                was_running = self.game_running
                self.game_running = running
                self._reset_for_context("game start" if running else "game stop")
                if was_running and not running:
                    self.game_running = False
                return
        if old is not _MISSING and old != value:
            self._reset_for_context(name.rsplit(".", 1)[-1] + " changed")

    def _reset_for_context(self, reason: str) -> None:
        LOG.info("Resetting popup baselines: %s", reason)
        target = self.return_page if self.in_popup_sequence else None
        self._cancel_sequence()
        self._clear_baselines()
        if target:
            self.desired_page = target
            self._start_navigator()

    def _handle_setting(self, property_name: str, value: Any) -> None:
        index, setting = self.setting_by_property[property_name]
        numeric = self._as_number(value)
        if not self.feed_connected or not self.wheel_connected or not self.game_running:
            self.baselines[property_name] = None
            return
        if numeric is None or (numeric < 0 and not setting.get("allow_negative", False)):
            self.baselines[property_name] = None
            return
        normalized = self._normalize(numeric, setting)
        previous = self.baselines[property_name]
        self.baselines[property_name] = normalized
        if previous is not None and normalized != previous:
            self.pending_changes.append((time.monotonic(), index, setting))

    def _normalize(self, value: float, setting: dict[str, Any]) -> float:
        if setting.get("percent_scale") and abs(value) <= 1:
            value *= 100
        return round(value, setting.get("decimals", 0))

    async def tick(self) -> None:
        now = time.monotonic()
        if self.pending_changes:
            newest_at = max(item[0] for item in self.pending_changes)
            if now - newest_at >= 0.08:
                _at, _index, setting = max(self.pending_changes,
                                            key=lambda item: (item[0], -item[1]))
                self.pending_changes.clear()
                self._show_popup(setting)
        if self.deadline is not None and now >= self.deadline:
            target = self.return_page
            LOG.info("Popup duration expired; restoring %s", target)
            self.deadline = None
            self.in_popup_sequence = False
            self.desired_page = target
            self._start_navigator()

    def _show_popup(self, setting: dict[str, Any]) -> None:
        if not self.in_popup_sequence:
            if self.active_page in self.mains:
                self.return_page = self.active_page
            elif self.last_main in self.mains:
                self.return_page = self.last_main
            else:
                LOG.warning("No main dashboard is known; popup change ignored")
                return
            self.in_popup_sequence = True
        self.deadline = time.monotonic() + self.config["popup_duration_seconds"]
        self.desired_page = setting["popup"]
        LOG.info("%s changed; showing %s for %.1f seconds (return: %s)",
                 setting["name"], setting["popup"],
                 self.config["popup_duration_seconds"], self.return_page)
        self._start_navigator()

    def _cancel_sequence(self) -> None:
        self.in_popup_sequence = False
        self.deadline = None
        self.return_page = None
        self.pending_changes.clear()

    def _clear_baselines(self) -> None:
        for name in self.baselines:
            self.baselines[name] = None
        self.pending_changes.clear()

    def _start_navigator(self) -> None:
        if not self.feed_connected or not self.wheel_connected or not self.desired_page:
            return
        if self.navigator is None or self.navigator.done():
            self.navigator = asyncio.create_task(self._navigate())
            self.navigator.add_done_callback(self._navigation_finished)

    def _navigation_finished(self, task: asyncio.Task) -> None:
        if self.navigator is task:
            self.navigator = None
        if task.cancelled():
            return
        error = task.exception()
        if error is not None:
            LOG.error("Dashboard navigation stopped unexpectedly: %s", error)
            self.desired_page = None
            return
        if self.desired_page and self.active_page != self.desired_page:
            self._start_navigator()

    async def _navigate(self) -> None:
        while self.desired_page and self.feed_connected and self.wheel_connected:
            target = self.desired_page
            if target not in self.order:
                LOG.error("Target dashboard %r is not in dashboard_order", target)
                self.desired_page = None
                return
            if self.active_page not in self.order:
                LOG.warning("Waiting for AZOM.DashboardName before navigating")
                self.desired_page = None
                return
            if self.active_page == target:
                self.desired_page = None
                return

            current_index = self.order.index(self.active_page)
            target_index = self.order.index(target)
            next_distance = (target_index - current_index) % len(self.order)
            previous_distance = (current_index - target_index) % len(self.order)
            direction = 1 if next_distance <= previous_distance else -1
            next_index = (current_index + direction) % len(self.order)
            next_name = self.order[next_index]
            self.expected_page = next_name
            self.page_event.clear()
            revision = self.page_revision
            try:
                await self._trigger_dashboard_action(direction)
                await asyncio.wait_for(self._wait_for_page_revision(revision),
                                       timeout=self.config["page_change_timeout_seconds"])
            except (OSError, asyncio.TimeoutError) as exc:
                LOG.error("Dashboard navigation failed at %s: %s", next_name, exc)
                self.expected_page = None
                self.desired_page = None
                return
            if self.active_page != next_name:
                self.desired_page = None
                return

    async def _wait_for_page_revision(self, revision: int) -> None:
        while self.page_revision <= revision:
            await self.page_event.wait()
            self.page_event.clear()

    async def _trigger_dashboard_action(self, direction: int) -> None:
        action = "AZOM.DashboardNext" if direction > 0 else "AZOM.DashboardPrev"
        process = await asyncio.create_subprocess_exec(
            self.config["simhub_exe"], "-triggeraction", action,
            stdout=asyncio.subprocess.DEVNULL, stderr=asyncio.subprocess.DEVNULL)
        code = await asyncio.wait_for(process.wait(), timeout=10)
        if code != 0:
            raise OSError(f"SimHub action command exited with code {code}")

    @staticmethod
    def _as_number(value: Any) -> float | None:
        if value is None or isinstance(value, bool):
            return None
        try:
            number = float(value)
        except (TypeError, ValueError):
            return None
        return number if math.isfinite(number) else None

    @staticmethod
    def _as_bool(value: Any) -> bool | None:
        if isinstance(value, bool):
            return value
        if isinstance(value, (int, float)):
            return value != 0
        if isinstance(value, str):
            normalized = value.strip().lower()
            if normalized in ("true", "1", "yes", "on"):
                return True
            if normalized in ("false", "0", "no", "off"):
                return False
        return None


_MISSING = object()


def validate_config(config: dict[str, Any]) -> None:
    order = config["dashboard_order"]
    mains = config["main_dashboards"]
    if len(order) != 8 or len(order) != len(set(order)):
        raise ValueError("dashboard_order must list each of the eight unique dashboards once")
    if len(mains) != 2 or any(name not in order for name in mains):
        raise ValueError("main_dashboards must contain the two main dashboard names")
    if config["popup_duration_seconds"] <= 0 or config["page_change_timeout_seconds"] <= 0:
        raise ValueError("timeouts must be positive")
    if any(item["popup"] not in order for item in config["settings"]):
        raise ValueError("every setting popup must appear in dashboard_order")


async def run(config: dict[str, Any]) -> None:
    validate_config(config)
    queue: asyncio.Queue[tuple[str, Any]] = asyncio.Queue()
    controller = DashboardController(config, queue)
    feed = PropertyFeed(config["property_server_host"], config["property_server_port"],
                        controller.required_properties(), queue)
    feed_task = asyncio.create_task(feed.run())
    LOG.info("Controller running; dashboard duration %.1fs", config["popup_duration_seconds"])
    try:
        while True:
            try:
                name, value = await asyncio.wait_for(queue.get(), timeout=0.05)
                await controller.handle(name, value)
            except asyncio.TimeoutError:
                pass
            await controller.tick()
    finally:
        feed_task.cancel()
        try:
            await feed_task
        except asyncio.CancelledError:
            pass


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path,
                        default=Path(__file__).with_name("controller.json"))
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(levelname)s %(message)s")
    try:
        config = json.loads(args.config.read_text(encoding="utf-8"))
        asyncio.run(run(config))
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    main()
