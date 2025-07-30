# Licensed under the GNU Lesser General Public License v3.0.
# ezudesign Copyright (C) 2023 numlinka.

__all__ = [
    "TASK_FLOW_START",
    "TASK_FLOW_EXEC",
    "TASK_FLOW_STOP",
    "TASK_FLOW_END",
    "TASK_FLOW_EXCEPT",
    "StopTaskFlow",
    "TaskItem",
    "TaskFlowDefaultAction",
    "TaskFlow"
]

# std
import copy
import threading

from typing import Optional, Iterable, Mapping, Callable, Any
from dataclasses import dataclass

# site
from typex import Static, MultitonAtomic


TASK_FLOW_ADD = "task_flow_add"
TASK_FLOW_REMOVE = "task_flow_remove"
TASK_FLOW_START = "task_flow_start"
TASK_FLOW_EXEC = "task_flow_exec"
TASK_FLOW_STOP = "task_flow_stop"
TASK_FLOW_END = "task_flow_end"
TASK_FLOW_EXCEPT = "task_flow_except"


@dataclass(frozen=True)
class TaskItem (object):
    iid: int
    task: Callable
    priority: int
    name: str
    async_: bool


class StopTaskFlow (Exception): ...


class TaskFlowDefaultAction (Static):
    @staticmethod
    def callback(self: "TaskFlow", action: str, detail: Optional[TaskItem | Exception] = None) -> None:
        ...

    @staticmethod
    def exec_async_task(self: "TaskFlow", taskunit: TaskItem, args: Iterable[Any], kwargs: Mapping[str, Any]) -> None:
        threading.Thread(None, taskunit.task, f"{self.name} - {taskunit.name} # {taskunit.iid}", args, kwargs).start()

    @staticmethod
    def exec_sync_task(self: "TaskFlow", taskunit: TaskItem, args: Iterable[Any], kwargs: Mapping[str, Any]) -> None:
        taskunit.task(*args, **kwargs)


class TaskFlow (object):
    def __init__(self, name: Optional[str] = None) -> None:
        self._lock = threading.RLock()
        self.__name = type(self).__name__ if name is None else name
        self.__atomic = MultitonAtomic(instance_name="numlinka - ezudesign - TaskFlow")
        self.__tasks: list[TaskItem] = []

    @property
    def name(self) -> str:
        with self._lock:
            return self.__name

    def callback(self, action: str, detail: Optional[TaskItem | Exception] = None) -> None:
        TaskFlowDefaultAction.callback(self, action, detail)

    def set_name(self, name: str) -> None:
        if not isinstance(name, str):
            raise TypeError(f"Expected `name` to be str, but got {type(name)}.")

        with self._lock:
            self.__name = name

    def __sort_key(self, item: TaskItem) -> int:
        return item.priority * 2 + (0 if item.async_ else 1)

    def add_task(self, task: Callable, priority: int = 1000, name: Optional[str] = None, async_: bool = False) -> int:
        if not callable(task):
            raise TypeError(f"Expected `task` to be callable, but got {type(task)}.")

        if not isinstance(name, str) and name is not None:
            raise TypeError(f"Expected `name` to be str or None, but got {type(name)}.")

        if not isinstance(priority, int):
            raise TypeError(f"Expected `priority` to be int, but got {type(priority)}.")

        if not 0 <= priority <= 10000:
            raise ValueError(f"Expected `priority` to be in range [0, 1000], but got {priority}.")

        if not isinstance(async_, bool):
            raise TypeError(f"Expected `async_`to be bool, but got {type(async_)}.")

        if name is None:
            name = task.__name__

        iid = self.__atomic.value
        item = TaskItem(iid, task, priority, name, async_)
        self.callback(TASK_FLOW_ADD, item)

        with self._lock:
            self.__tasks.append(item)
            self.__tasks.sort(key=self.__sort_key)

        return iid

    def remove_task(self, anymark: int | str | Callable) -> bool:
        if not isinstance(anymark, (int, str)) and not callable(anymark):
            raise TypeError(f"Expected `anymark` to be int, str or callable, but got {type(anymark)}.")

        with self._lock:
            index = -1

            for i, item in enumerate(self.__tasks):
                if isinstance(anymark, int):
                    if item.iid == anymark:
                        index = i
                        break

                elif isinstance(anymark, str):
                    if item.name == anymark:
                        index = i
                        break

                else:
                    if item.task == anymark:
                        index = i
                        break

            if index == -1:
                return False

            del self.__tasks[index]
            self.callback(TASK_FLOW_REMOVE, item)
            return True

    def _exec_async_task(self, taskunit: TaskItem, args: Iterable[Any], kwargs: Mapping[str, Any]) -> None:
        self.callback(TASK_FLOW_EXEC, taskunit)
        TaskFlowDefaultAction.exec_async_task(self, taskunit, args, kwargs)

    def _exec_sync_task(self, taskunit: TaskItem, args: Iterable[Any], kwargs: Mapping[str, Any]) -> None:
        self.callback(TASK_FLOW_EXEC, taskunit)
        TaskFlowDefaultAction.exec_sync_task(self, taskunit, args, kwargs)

    def run(self, *args, **kwargs) -> None:
        self.callback(TASK_FLOW_START)
        with self._lock:
            copy_tasks = copy.copy(self.__tasks)

        try:
            for item in copy_tasks:
                if item.async_:
                    self._exec_async_task(item, args, kwargs)
                else:
                    self._exec_sync_task(item, args, kwargs)

            else:
                self.callback(TASK_FLOW_END)

        except StopTaskFlow:
            self.callback(TASK_FLOW_STOP, (item))

        except Exception as e:
            self.callback(TASK_FLOW_EXCEPT, e)
            raise e

    def __call__(self, *args, **kwargs):
        self.run(*args, **kwargs)
