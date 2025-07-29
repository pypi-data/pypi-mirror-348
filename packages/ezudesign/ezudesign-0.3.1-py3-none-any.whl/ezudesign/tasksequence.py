# Licensed under the GNU Lesser General Public License v3.0.
# ezudesign Copyright (C) 2023 numlinka.

# std
import threading

from typing import Callable, Iterable, Mapping, Optional, Any, NoReturn
from dataclasses import dataclass

# site
from typex import MultitonAtomic


TASK_SEQUENCE_START = "task_sequence_start"
TASK_SEQUENCE_ADD = "task_sequence_add"
TASK_SEQUENCE_EXEC = "task_sequence_exec"
TASK_SEQUENCE_IDLE = "task_sequence_idle"
TASK_SEQUENCE_EXCEPT = "task_sequence_except"
TASK_SEQUENCE_CLEAR = "task_sequence_clear"


@dataclass
class SyncTaskUnit (object):
    iid: int
    name: str
    task: Callable
    args: Iterable[Any]
    kwargs: Mapping[str, Any]


class TaskSequence (object):
    def __init__(self):
        self._lock = threading.RLock()
        self.thread: Optional[threading.Thread] = None
        self._event = threading.Event()
        self.__atomic = MultitonAtomic(instance_name="numlinka - ezudesign - TaskSequence")
        self.__task_list: list[SyncTaskUnit]

    @property
    def running(self) -> bool:
        return self.thread is not None and self.thread.is_alive()

    def callback(self, action: str, detail: Optional[SyncTaskUnit | Exception] = None) -> None:
        ...

    def add_task(self, name: str, task: Callable, args: Iterable[Any], kwargs: Mapping[str, Any]) -> int:
        if not isinstance(name, str):
            raise TypeError(f"Expected `name` to be str, but got {type(name)}.")

        if not callable(task):
            raise TypeError(f"Expected `task` to be callable, but got {type(task)}.")

        if not isinstance(args, Iterable) and args is not None:
            raise TypeError(f"Expected `args` to be Iterable, but got {type(args)}.")

        if not isinstance(kwargs, Mapping) and kwargs is not None:
            raise TypeError(f"Expected `kwargs` to be Mapping, but got {type(kwargs)}.")

        iid = self.__atomic.value
        unit = SyncTaskUnit(iid, name, task, args, kwargs)
        with self._lock:
            self.__task_list.append(unit)

        self.callback(TASK_SEQUENCE_ADD, unit)
        return iid

    def clear(self) -> None:
        with self._lock:
            self.__task_list.clear()

        self.callback(TASK_SEQUENCE_CLEAR)

    def __run(self) -> NoReturn:
        while True:
            try:
                self._event.wait()

                with self._lock:
                    if not self.__task_list:
                        self._event.clear()
                        self.callback(TASK_SEQUENCE_IDLE)
                        continue

                    unit = self.__task_list.pop(0)

                self.callback(TASK_SEQUENCE_EXEC, unit)
                unit.task(*unit.args, **unit.kwargs)

            except Exception as e:
                self._event.clear()
                self.clear()
                self.callback(TASK_SEQUENCE_EXCEPT, e)
                continue

    def start(self) -> bool:
        with self._lock:
            if self.thread is not None and self.thread.is_alive():
                return False

            self.thread = threading.Thread(None, self.__run, "Synchronization", (), {}, daemon=True)
            self.thread.start()

        self.callback(TASK_SEQUENCE_START)
        return True
