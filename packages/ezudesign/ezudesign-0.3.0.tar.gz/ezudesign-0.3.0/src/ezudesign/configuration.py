# Licensed under the GNU Lesser General Public License v3.0.
# ezudesign Copyright (C) 2023 numlinka.

__all__ = [
    "ConfigurationBaseException",
    "ConfigKeyDoesNotExist",
    "ConfigKeyAlreadyExist",
    "ConfigValueOutOfRange",
    "ConfigFileTypeNotSpecified",
    "ConfigItem",
    "NumericalRange",
    "Variable",
    "IntVariable",
    "FloatVariable",
    "StrVariable",
    "Configuration",
    "ConfigurationControl",
    "setting"
]

# std
import copy
import json
import inspect
import threading

from base64 import b64encode, b64decode
from typing import Iterable, Mapping, Optional, Type
from dataclasses import dataclass, field

# site
from typex import Static


class ConfigurationBaseException (Exception): ...
class ConfigKeyDoesNotExist (ConfigurationBaseException): ...
class ConfigKeyAlreadyExist (ConfigurationBaseException): ...
class ConfigValueOutOfRange (ConfigurationBaseException): ...
class ConfigFileTypeNotSpecified (ConfigurationBaseException): ...
class ConfigFileTypeNotSupported (ConfigurationBaseException): ...


class ConfigFileType (Static):
    JSON = "json"


@dataclass
class ConfigItem (object):
    type_: Type[int | float | str]
    default: Optional[int | float | str] = field(default=None)
    ranges: Optional[Iterable[int | float | str]] = field(default=None)
    value: Optional[int | float | str] = field(default=None)


@dataclass
class NumericalRange (object):
    min: int | float
    max: int | float
    float_round: int = field(default=0)

    def __post_init__(self):
        if not isinstance(self.min, (int, float)):
            raise TypeError(f"Expected `min` to be `int` or `float`, but got {type(self.min)}.")

        if not isinstance(self.max, (int, float)):
            raise TypeError(f"Expected `max` to be `int` or `float`, but got {type(self.max)}.")

        if not isinstance(self.float_round, int):
            raise TypeError(f"Expected `float_round` to be `int`, but got {type(self.float_round)}.")
        
        if self.float_round < 0:
            raise ValueError(f"Expected `float_round` to be greater than or equal to 0, but got {self.float_round}.")


@dataclass
class LastState (object):
    filepath: Optional[str] = field(default=None)
    filetype: Optional[str] = field(default=None)
    encoding: str = field(default="utf-8")
    base64: bool = field(default=False)


class Variable (object):
    def __new__(cls, stem: "ConfigurationControl", key: str, value: int | float | str) -> "Variable":
        if cls is Variable:
            raise TypeError("Cannot create an instance of the abstract class Variable.")

        instance = super(Variable, cls).__new__(cls, value)
        instance.__set_attribute(stem, key)

        return instance

    def __set_attribute(self, stem: "ConfigurationControl", key: str) -> None:
        self.__stem = stem
        self.__key = key

    @property
    def ranges(self) -> Optional[Iterable[int | float | str] | NumericalRange]:
        return self.__stem.get_ranges(self.__key)

    @property
    def value(self) -> int | float | str:
        return self.__stem.get(self.__key)

    @property
    def stem(self) -> "Configuration":
        return self.__stem.surface

    @property
    def name(self) -> str:
        return self.__key

    def set(self, value: int | float | str) -> None:
        self.__stem.set(self.__key, value)


class IntVariable (Variable, int): ...


class FloatVariable (Variable, float): ...


class StrVariable (Variable, str): ...


class Configuration (object):
    def __init__(self):
        self.ctrl = ConfigurationControl(self)
        items = [x for x in dir(self) if not x.startswith("_") and x != "ctrl"]
        getattribute = super().__getattribute__
        for name in items:
            item = getattribute(name)
            if not isinstance(item, ConfigItem):
                continue

            self.ctrl.new(name, item.type_, item.default, item.ranges)

    def __setattr__(self, name, value) -> None:
        if name.startswith("_") or name == "ctrl":
            return super().__setattr__(name, value)

        self.ctrl.set(name, value)

    def __setitem__(self, name, value) -> None:
        self.ctrl.set(name, value)

    def __getitem__(self, name) -> "Variable":
        return self.ctrl.get(name)

    def __getattribute__(self, name) -> "Variable":
        if name.startswith("_") or name == "ctrl":
            return super().__getattribute__(name)

        return self.ctrl.get(name)


class ConfigurationControl (object):
    def __init__(self, surface: Configuration):
        self.surface = surface
        self._lock = threading.RLock()
        self.__table: Mapping[str, ConfigItem] = {}
        self.__invalid: Mapping[str, int | float | str] = {}
        self.__last = LastState()

    @property
    def last_filepath(self) -> Optional[str]:
        with self._lock:
            return self.__last.filepath

    @property
    def last_filetype(self) -> Optional[str]:
        with self._lock:
            return self.__last.filetype

    @property
    def last_encoding(self) -> str:
        with self._lock:
            return self.__last.encoding

    @property
    def last_base64(self) -> bool:
        with self._lock:
            return self.__last.base64

    def new(self, key: str, type_: Type[int | float | str], default: Optional[int | float | str] = None,
            ranges: Optional[Iterable[int | float | str] | NumericalRange] = None) -> None:
        if not isinstance(key, str):
            raise TypeError(f"Expected `key` to be `str`, but got {type(key)}.")

        if inspect.isclass(type_) and not issubclass(type_, (int, float, str)):
            raise TypeError(f"Expected `type_` to be `int`, `float` or `str` class, but got {type(type_)}.")

        if not isinstance(default, type_) and default is not None:
            raise TypeError(f"Expected `default` to be `{type_}` or None, but got {type(default)}.")

        if not isinstance(ranges, (Iterable, NumericalRange)) and not ranges is None:
            raise TypeError(f"Expected `ranges` to be Iterable or NumericalRange, but got {type(ranges)}.")

        with self._lock:
            if key in self.__table:
                raise ConfigKeyAlreadyExist(f"The config key `{key}` already exists.")

            default = default if default is not None else type_()
            self.__table[key] = ConfigItem(type_, default, ranges, None)

    def set(self, key: str, value: Optional[int | float | str] = None) -> None :
        if not isinstance(key, str):
            raise TypeError(f"Expected `key` to be `str`, but got {type(key)}.")

        if not isinstance(value, (int, float, str)) and value is not None:
            raise TypeError(f"Expected `value` to be `int`, `float` or `str`, but got {type(value)}.")

        if value is None:
            return

        with self._lock:
            if key not in self.__table:
                self.__invalid[key] = value
                return

            item = self.__table[key]
            if not isinstance(value, item.type_):
                raise TypeError(f"The value `{value}` is inconsistent with the constraint type.")

            if (isinstance(item.ranges, NumericalRange) and not (item.ranges.min <= value <= item.ranges.max)) or \
               (isinstance(item.ranges, Iterable) and value not in item.ranges):
                raise ConfigValueOutOfRange(f"The value `{value}` is inconsistent with the constraint ranges.")

            if item.type_ is float and isinstance(item.ranges, NumericalRange) and item.ranges != 0:
                value = round(value, item.ranges.float_round)

            self.__table[key].value = value

    def set_ranges(self, key: str, ranges: Iterable[int | float | str] | NumericalRange):
        if not isinstance(key, str):
            raise TypeError(f"Expected `key` to be `str`, but got {type(key)}.")

        if not isinstance(ranges, (Iterable, NumericalRange)):
            raise TypeError(f"Expected `ranges` to be Iterable, but got {type(ranges)}.")

        with self._lock:
            if key not in self.__table:
                raise ConfigKeyDoesNotExist(f"The config key `{key}` does not exist.")

            item = self.__table[key]
            item.ranges = ranges

    def get(self, key: str) -> "Variable":
        if not isinstance(key, str):
            raise TypeError(f"Expected `key` to be `str`, but got {type(key)}.")

        with self._lock:
            if key in self.__table:
                item = self.__table[key]
                value = item.default if item.value is None else item.value
                return _VARIABLE_CLASS_TABLE[item.type_](self, key, value)

            elif key in self.__invalid:
                return self.__invalid[key]

            raise ConfigKeyDoesNotExist(f"The config key `{key}` does not exist.")

    def get_ranges(self, key: str) -> Optional[Iterable[int | float | str] | NumericalRange]:
        if not isinstance(key, str):
            raise TypeError(f"Expected `key` to be `str`, but got {type(key)}.")

        with self._lock:
            if key not in self.__table:
                raise ConfigKeyDoesNotExist(f"The config key `{key}` does not exist.")

            item = self.__table[key]
            return copy.copy(item.ranges)

    def load_dict(self, data: Mapping) -> list[str]:
        if not isinstance(data, Mapping):
            raise TypeError(f"Expected `data` to be `Mapping`, but got {type(data)}.")

        lst = []

        for key, value in data.items():
            try:
                self.set(key, value)

            except Exception as _:
                lst.append(key)

        return lst

    def load_json(self, filepath: str, encoding: str = "utf-8", *, base64: bool = False) -> list[str]:
        with open(filepath, "r", encoding=encoding) as file_obj:
            content = file_obj.read()
            if base64:
                content = b64decode(content).decode(encoding)
            data = json.loads(content)

        with self._lock:
            self.__last.filepath = filepath
            self.__last.filetype = ConfigFileType.JSON
            self.__last.encoding = encoding
            self.__last.base64 = base64

        return self.load_dict(data)

    def save(self, filepath: Optional[str] = None, filetype: Optional[str] = None,
             encoding: Optional[str] = None, *, base64: Optional[bool] = None) -> None:
        if not isinstance(filepath, str) and filepath is not None:
            raise TypeError(f"Expected `filepath` to be `str` or None, but got {type(filepath)}.")

        if not isinstance(filetype, str) and filetype is not None:
            raise TypeError(f"Expected `filetype` to be `str` or None, but got {type(filetype)}.")

        if not isinstance(encoding, str) and encoding is not None:
            raise TypeError(f"Expected `encoding` to be `str` or None, but got {type(encoding)}.")

        if not isinstance(base64, bool) and base64 is not None:
            raise TypeError(f"Expected `base64` to be `bool` or None, but got {type(base64)}.")

        filepath = filepath or self.last_filepath
        filetype = filetype or self.last_filetype
        encoding = encoding or self.last_encoding
        base64 = self.last_base64 if base64 is None else base64

        if filepath is None or filetype is None:
            raise ConfigFileTypeNotSpecified(f"The config file type is not specified.")

        match filetype:
            case ConfigFileType.JSON:
                self.save_json(filepath, encoding, base64=base64)

            case _:
                raise ConfigFileTypeNotSupported(f"The config file type `{filetype}` is not supported.")

    def save_json(self, filepath: str, encoding: str = "utf-8", *, base64: bool = False) -> None:
        with self._lock:
            data = {key: item.value for key, item in self.__table.items()}

        if not base64:
            content = json.dumps(data, ensure_ascii=False, sort_keys=False, indent=4)

            with open(filepath, "w", encoding=encoding) as fobj:
                fobj.write(content)
            return

        content = json.dumps(data, ensure_ascii=False, sort_keys=False)
        content = b64encode(content.encode(encoding))
        with open(filepath, "wb") as fobj:
            fobj.write(content)


def setting(
        type_: int | float | str,
        default: Optional[int | float | str] = None,
        ranges: Optional[Iterable[int | float | str]] = None
        ) -> Variable:
    # ! ConfigItem 会在 Configuration 中变换为 Variable 对象,
    # ! 且你不应该在 Configuration 之外使用 setting 函数,
    # ! 因此这里将函数返回类型标注为 Variable 而不是 ConfigItem 以欺骗类型检查.
    return ConfigItem(type_, default, ranges)


_VARIABLE_CLASS_TABLE = {
    int: IntVariable,
    float: FloatVariable,
    str: StrVariable
}
