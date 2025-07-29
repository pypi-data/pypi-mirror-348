# Licensed under the GNU Lesser General Public License v3.0.
# ezudesign Copyright (C) 2023 numlinka.

__all__ = ["ExecItem", "try_exec", "exec_item"]

# std
from typing import Callable, Iterable, Mapping, Optional, Any
from dataclasses import dataclass, field


@dataclass(frozen=True)
class ExecItem (object):
    callback: Callable
    args: Iterable[Any] = field(default_factory=tuple)
    kwargs: Mapping[str, Any] = field(default_factory=dict)


def try_exec(exec_try: ExecItem, exec_except: Optional[ExecItem] = None) -> Any:
    if not isinstance(exec_try, ExecItem):
        raise TypeError(f"Expected `exec_try` to be ExecItem, but got {type(exec_try)}.")

    if not isinstance(exec_except, ExecItem) and exec_except is not None:
        raise TypeError(f"Expected `exec_except` to be ExecItem, but got {type(exec_except)}.")

    try:
        return exec_try.callback(*exec_try.args, **exec_try.kwargs)

    except Exception as e:
        if exec_except is not None:
            return exec_except.callback(e, *exec_except.args, **exec_except.kwargs)

        return e


def exec_item(callback: Callable, *args: Any, **kwargs: Any) -> ExecItem:
    return ExecItem(callback, args, kwargs)
