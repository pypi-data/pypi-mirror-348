# Licensed under the GNU Lesser General Public License v3.0.
# ezudesign Copyright (C) 2023 numlinka.

__all__ = [
    "EVENT_HUB_EMIT",
    "EVENT_HUB_SUBSCRIBE",
    "EVENT_HUB_UNSUBSCRIBE",
    "EVENT_HUB_EXCEPTION",
    "EVENT_HUB_EXEC",
    "EventHubBaseException",
    "EventNameDoesNotExist",
    "EventItem",
    "EventHubDefaultAction",
    "EventHub"
]

# std
import threading

from typing import Any, Callable, Iterable, Mapping, Optional
from dataclasses import dataclass

# site
from typex import Static, MultitonAtomic


EVENT_HUB_EMIT = "event_hub_emit"
EVENT_HUB_SUBSCRIBE = "event_hub_subscribe"
EVENT_HUB_UNSUBSCRIBE = "event_hub_unsubscribe"
EVENT_HUB_EXCEPTION = "event_hub_exception"
EVENT_HUB_EXEC = "event_hub_exec"


class EventHubBaseException (Exception): ...
class EventNameDoesNotExist (EventHubBaseException): ...


@dataclass(frozen=True)
class EventItem (object):
    iid: int
    event_name: str
    callback: Callable
    args: Iterable[Any]
    kwargs: Mapping[str, Any]
    is_async: bool


class EventHubDefaultAction (Static):
    @staticmethod
    def callback(action: str, detail: Optional[EventItem | Exception] = None) -> None:
        ...

    @staticmethod
    def exec_async_task(event_item: EventItem) -> None:
        threading.Thread(None, event_item.callback, f"{event_item.event_name} # {event_item.iid}",
                         event_item.args, event_item.kwargs).start()

    @staticmethod
    def exec_sync_task(event_item: EventItem) -> None:
        event_item.callback(*event_item.args, **event_item.kwargs)


class EventHub (object):
    def __init__(self, event_list: Optional[Iterable[str]] = None) -> None:
        if not isinstance(event_list, Iterable):
            raise TypeError(f"Expected `event_list` to be Iterable, but got {type(event_list)}.")

        self._lock = threading.RLock()
        self.__atomic = MultitonAtomic(instance_name="numlinka - ezudesign - EventHub")
        self.__event_list = []
        self.__subscribe: dict[int, EventItem] = {}
        self.__wait: dict[str, list[threading.Event]] = {}

        for event_name in event_list or []:
            self.add_event(event_name)

    def callback(self, action: str, detail: Optional[EventItem | Exception] = None) -> None:
        EventHubDefaultAction.callback(action, detail)

    def add_event(self, event_name: str) -> None:
        if not isinstance(event_name, str):
            raise TypeError(f"Expected `event_name` to be str, but got {type(event_name)}.")

        with self._lock:
            if event_name not in self.__event_list:
                self.__event_list.append(event_name)

    def wait(self, event_name: str, timeout: Optional[int | float] = None) -> bool:
        if not isinstance(event_name, str):
            raise TypeError(f"Expected `event_name` to be str, but got {type(event_name)}.")

        if not isinstance(timeout, (int, float)) and timeout is not None:
            raise TypeError(f"Expected `timeout` to be int or float, but got {type(timeout)}.")

        with self._lock:
            if event_name not in self.__event_list:
                raise EventNameDoesNotExist(f"Event name `{event_name}` does not exist.")

            if event_name not in self.__wait:
                self.__wait[event_name] = []

            unit = threading.Event()
            self.__wait[event_name].append(unit)

        return unit.wait(timeout)

    def subscribe(self, event_name: str, callback: Callable, args: Optional[Iterable[Any]] = None,
                  kwargs: Optional[Mapping[str, Any]] = None, async_: bool = False) -> int:
        if not isinstance(event_name, str):
            raise TypeError(f"Expected `event_name` to be str, but got {type(event_name)}.")

        if not callable(callback):
            raise TypeError(f"Expected `callback` to be callable, but got {type(callback)}.")

        if not isinstance(args, Iterable) and args is not None:
            raise TypeError(f"Expected `args` to be Iterable, but got {type(args)}.")

        if not isinstance(kwargs, Mapping) and kwargs is not None:
            raise TypeError(f"Expected `kwargs` to be Mapping, but got {type(kwargs)}.")

        with self._lock:
            if event_name not in self.__event_list:
                raise EventNameDoesNotExist(f"Event name `{event_name}` does not exist.")

            iid = self.__atomic.value
            item = EventItem(iid, event_name, callback, args or [], kwargs or {}, async_)
            self.__subscribe[iid] = item

        self.callback(EVENT_HUB_SUBSCRIBE, item)
        return iid

    def unsubscribe(self, anymark: int | Callable) -> bool:
        if isinstance(anymark, int):
            with self._lock:
                if anymark in self.__subscribe:
                    item = self.__subscribe[anymark]
                    del self.__subscribe[anymark]

                else:
                    return False

            self.callback(EVENT_HUB_UNSUBSCRIBE, item)

        elif callable(anymark):
            with self._lock:
                for iid, item in self.__subscribe.items():
                    if item.callback == anymark:
                        item = self.__subscribe[iid]
                        del self.__subscribe[iid]
                        break

                else:
                    return False

            self.callback(EVENT_HUB_UNSUBSCRIBE, item)

        else:
            raise TypeError(f"Expected `anymark` to be int or callable, but got {type(anymark)}.")

    def _exec_async_task(self, event_item: EventItem) -> None:
        self.callback(EVENT_HUB_EXEC, event_item)
        EventHubDefaultAction.exec_async_task(event_item)

    def _exec_sync_task(self, event_item: EventItem) -> None:
        self.callback(EVENT_HUB_EXEC, event_item)
        EventHubDefaultAction.exec_sync_task(event_item)

    def emit(self, event_name: str) -> None:
        if not isinstance(event_name, str):
            raise TypeError(f"Expected `event_name` to be str, but got {type(event_name)}.")

        self.callback(EVENT_HUB_EMIT, event_name)
        list_wait = []
        list_async: list[EventItem] = []
        list_sync: list[EventItem] = []

        with self._lock:
            if event_name not in self.__event_list:
                raise EventNameDoesNotExist(f"Event name `{event_name}` does not exist.")

            if event_name in self.__wait:
                list_wait = self.__wait[event_name]
                self.__wait[event_name] = []

            for _, item in self.__subscribe.items():
                if item.event_name == event_name:
                    if item.is_async:
                        list_async.append(item)
                    else:
                        list_sync.append(item)

        for wait_event in list_wait:
            wait_event.set()

        try:
            for item in list_async:
                self._exec_async_task(item)

            for item in list_sync:
                self._exec_sync_task(item)

        except Exception as e:
            # ! 调用错误不应由触发事件的函数承担
            self.callback(EVENT_HUB_EXCEPTION, e)

    listen = subscribe
    fire = emit
