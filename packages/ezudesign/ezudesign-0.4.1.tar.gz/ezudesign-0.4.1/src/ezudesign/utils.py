# Licensed under the GNU Lesser General Public License v3.0.
# ezudesign Copyright (C) 2023 numlinka.

__all__ = ["ExecItem", "try_exec", "exec_item"]

# std
import inspect
from typing import Callable, Iterable, Mapping, Optional, Any
from dataclasses import dataclass, field

@dataclass(frozen=True)
class ExecItem (object):
    callback: Callable | str
    args: Iterable[Any] = field(default_factory=tuple)
    kwargs: Mapping[str, Any] = field(default_factory=dict)


def try_exec(exec_try: ExecItem, exec_except: Optional[ExecItem] = None) -> Any:
    if not isinstance(exec_try, (ExecItem, str)):
        raise TypeError(f"Expected `exec_try` to be ExecItem, but got {type(exec_try)}.")

    if not isinstance(exec_except, ExecItem) and exec_except is not None:
        raise TypeError(f"Expected `exec_except` to be ExecItem, but got {type(exec_except)}.")

    try:
        if callable(exec_try.callback):
            try_callable = exec_try.callback

        elif isinstance(exec_try.callback, str):
            attr_names = exec_try.callback.split(".")
            frame = inspect.currentframe().f_back
            for index, attr_name in enumerate(attr_names):
                if index == 0:
                    if attr_name in frame.f_locals.keys():
                        obj = frame.f_locals[attr_name]
                    elif attr_name in frame.f_globals.keys():
                        obj = frame.f_globals[attr_name]
                    else:
                        raise NameError
                    continue
                obj = getattr(obj, attr_name)

            else:
                try_callable = obj

        else:
            raise TypeError

        return try_callable(*exec_try.args, **exec_try.kwargs)

    except Exception as e:
        if exec_except is not None:
            return exec_except.callback(e, *exec_except.args, **exec_except.kwargs)

        return e


def exec_item(callback: Callable, *args: Any, **kwargs: Any) -> ExecItem:
    return ExecItem(callback, args, kwargs)


# try_exec(exec_item("self"))
