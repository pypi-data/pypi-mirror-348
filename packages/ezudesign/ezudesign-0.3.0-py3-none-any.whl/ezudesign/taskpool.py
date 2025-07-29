# Licensed under the GNU Lesser General Public License v3.0.
# ezudesign Copyright (C) 2023 numlinka.

# std
import threading

from typing import Callable, Any, Iterable, Mapping, Optional, NoReturn
from dataclasses import dataclass, field

# site
from typex import MultitonAtomic


TASKPOOL_NEW_TASK = "task_pool_new_task"
TASKPOOL_TASK_START = "task_pool_task_start"
TASKPOOL_TASK_DONE = "task_pool_task_done"
TASKPOOL_TASK_EXCEPT = "task_pool_task_except"


@dataclass
class TaskUnit (object):
    iid: int
    task: Callable
    args: Iterable
    kwargs: Mapping
    need_return: bool
    event: threading.Event = field(default_factory=threading.Event)
    exception: Optional[Exception] = None
    result: Optional[Any] = None


@dataclass
class ThreadUnit (object):
    tpid: int
    thread: threading.Thread
    task: Optional[TaskUnit] = None
    work: threading.Event = field(default_factory=threading.Event)
    done: threading.Event = field(default_factory=threading.Event)


class TaskPool (object):
    def __init__ (self, size: int = 16) -> None:
        self._lock = threading.RLock()
        self.__queue_task: list[TaskUnit] = []
        self.__queue_running: list[TaskUnit] = []
        self.__queue_done: list[TaskUnit] = []
        self.__pool: list[ThreadUnit] = []
        self.__size: int = size

        self.__atomic = MultitonAtomic(instance_name="numlinka - ezudesign - TaskPool/TaskID")
        self.__atomic_tpid = MultitonAtomic(instance_name="numlinka - ezudesign - TaskPool/ThreadID")

    def callback(self, action: str, detail: Optional[TaskUnit | Exception] = None) -> None:
        ...

    def new_task(self, task: Callable, args: Optional[Iterable[Any]] = None,
                 kwargs: Optional[Mapping[str, Any]] = None, need_return: bool = False) -> int:
        if not callable(task):
            raise TypeError(f"Expected `task` to be callable, but got {type(task)}.")

        if not isinstance(args, Iterable) and args is not None:
            raise TypeError(f"Expected `args` to be Iterable, but got {type(args)}.")

        if not isinstance(kwargs, Mapping) and kwargs is not None:
            raise TypeError(f"Expected `kwargs` to be Mapping, but got {type(kwargs)}.")

        iid = self.__atomic.value

        unit = TaskUnit(
            iid=iid,
            task=task,
            args=args or (),
            kwargs=kwargs or {},
            need_return=need_return,
        )

        with self._lock:
            self.__queue_task.append(unit)

        self.callback(TASKPOOL_NEW_TASK, unit)
        self.__task_actvicate()
        return iid

    def join(self, iid: int, timeout: Optional[int | float] = None) -> bool:
        if not isinstance(iid, int):
            raise TypeError(f"Expected `iid` to be int, but got {type(iid)}.")

        if not isinstance(timeout, (int, float)) and timeout is not None:
            raise TypeError(f"Expected `timeout` to be int or float, but got {type(timeout)}.")

        with self._lock:
            for unit in self.__queue_task:
                if unit.iid == iid:
                    break

            else:
                for unit in self.__queue_running:
                    if unit.iid == iid:
                        break

                else:
                    return True

        unit.event.wait(timeout)

    def get_return(self, iid: int) -> Any:
        if not isinstance(iid, int):
            raise TypeError(f"Expected `iid` to be int, but got {type(iid)}.")

        with self._lock:
            for index, unit in enumerate(self.__queue_done):
                if unit.iid == iid:
                    break

            else:
                raise ValueError(f"The task with ID {iid} was not completed or was abandoned.")

            self.__queue_done.pop(index)

        return unit.result

    def __run_unit(self, unit: ThreadUnit) -> NoReturn:
        while True:
            try:
                unit.work.wait()
                unit.done.clear()

                if unit.task is None:
                    unit.work.clear()
                    unit.done.set()
                    continue

                self.callback(TASKPOOL_TASK_START, unit.task)
                result = unit.task.task(*unit.task.args, **unit.task.kwargs)
                if unit.task.need_return:
                    unit.task.result = result

            except Exception as e:
                self.callback(TASKPOOL_TASK_EXCEPT, unit.task)
                unit.task.exception = e

            else:
                self.callback(TASKPOOL_TASK_DONE, unit.task)

            finally:
                self.__task_done(unit.task)
                unit.task.event.set()
                unit.task = None
                unit.work.clear()
                unit.done.set()
                self.__task_actvicate()


    def __task_done(self, task_unit: TaskUnit) -> None:
        with self._lock:
            self.__queue_running.remove(task_unit)
            if not task_unit.need_return:
                return

            self.__queue_done.append(task_unit)

    def __task_actvicate(self) -> None:
        with self._lock:
            while True:
                if not self.__queue_task:
                    break

                for thread_unit in self.__pool:
                    if thread_unit.done.is_set():
                        break

                else:
                    if len(self.__pool) >= self.__size:
                        break
                    thread_unit = ThreadUnit(self.__atomic_tpid.value, ...)
                    self.__pool.append(thread_unit)
                    thread_unit.thread = threading.Thread(
                        None,
                        self.__run_unit,
                        f"TaskPool#{thread_unit.tpid}",
                        (thread_unit, ),
                        {},
                        daemon=True
                    )
                    thread_unit.thread.start()

                task_unit = self.__queue_task.pop(0)
                self.__queue_running.append(task_unit)
                thread_unit.done.clear()
                thread_unit.task = task_unit
                thread_unit.work.set()
