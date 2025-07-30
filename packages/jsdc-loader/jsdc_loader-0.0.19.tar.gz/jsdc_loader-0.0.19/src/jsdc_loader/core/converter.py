"""Conversion utilities for JSDC Loader."""

from typing import Any, Type, get_args, get_origin, Union, Dict, List, Set
from dataclasses import is_dataclass, fields, MISSING, Field
from enum import Enum
from pydantic import BaseModel
import inspect

from .types import T
from .validator import get_cached_type_hints, validate_type

def convert_enum(key: str, value: Any, enum_type: Type[Enum]) -> Enum:
    """Convert a string value to an Enum member."""
    try:
        return enum_type[value]
    except KeyError:
        raise ValueError(f'Invalid Enum value for key {key}: {value}')

def convert_union_type(key: str, value: Any, union_type: Any) -> Any:
    """Convert a value to one of the Union types."""
    args = get_args(union_type)
    non_none_args = [arg for arg in args if arg is not type(None)]
    if len(non_none_args) == 1:
        actual_type = non_none_args[0]
        if isinstance(actual_type, type) and issubclass(actual_type, Enum):
            return actual_type[value]
        else:
            return convert_value(key, value, actual_type)
    else:
        raise TypeError(f'Unsupported Union type for key {key}: {union_type}')

def convert_simple_type(key: str, value: Any, e_type: Any) -> Any:
    """Convert a value to a simple type."""
    if isinstance(e_type, type) and issubclass(e_type, Enum):
        return e_type[value]
    elif e_type == dict or get_origin(e_type) == dict:
        # Handle dict type properly
        return value
    elif e_type == list or get_origin(e_type) == list:
        # Handle list type properly
        return value
    else:
        try:
            return e_type(value)
        except TypeError:
            # If it's a typing.Dict or typing.List, just return the value
            if str(e_type).startswith('typing.'):
                return value
            raise

def convert_dict_type(key: str, value: dict, e_type: Any) -> dict:
    """Convert a dictionary based on its type annotation."""
    if get_origin(e_type) is dict:
        key_type, val_type = get_args(e_type)
        if key_type != str:
            raise ValueError(f"Only string keys are supported for dictionaries in key {key}")
        
        # If the value type is complex, process each item
        if is_dataclass(val_type) or get_origin(val_type) is Union:
            return {k: convert_value(f"{key}.{k}", v, val_type) for k, v in value.items()}
    
    # Default case, just return the dict
    return value

def convert_value(key: str, value: Any, e_type: Any) -> Any:
    """Convert a value to the expected type."""
    if value is None and get_origin(e_type) is Union and type(None) in get_args(e_type):
        return None
    
    # // 杂鱼♡～本喵在这里加了一段逻辑，如果期望的是 set 但得到的是 list，就把它转成 set 喵！～
    if (get_origin(e_type) is set or e_type is set) and isinstance(value, list):
        args = get_args(e_type)
        if args: # // 杂鱼♡～如果 set 里面有类型定义，比如 Set[Model]，那就要对每个元素进行转换喵～
            element_type = args[0]
            return {convert_value(f"{key}[*]", item, element_type) for item in value}
        else: # // 杂鱼♡～如果只是普通的 set，比如 Set[str]，就直接转喵～
            return set(value)

    if isinstance(e_type, type) and issubclass(e_type, Enum):
        return convert_enum(key, value, e_type)
    elif is_dataclass(e_type):
        return convert_dict_to_dataclass(value, e_type)
    elif get_origin(e_type) is list or e_type == list:
        args = get_args(e_type)
        if args and is_dataclass(args[0]):
            return [convert_dict_to_dataclass(item, args[0]) for item in value]
        elif args:
            return [convert_value(f"{key}[{i}]", item, args[0]) for i, item in enumerate(value)]
        return value
    elif get_origin(e_type) is dict or e_type == dict:
        return convert_dict_type(key, value, e_type)
    else:
        origin = get_origin(e_type)
        if origin is Union:
            return convert_union_type(key, value, e_type)
        else:
            return convert_simple_type(key, value, e_type)

# // 杂鱼♡～本喵添加了这个函数来检查一个dataclass是否是frozen的喵～
def is_frozen_dataclass(cls):
    """Check if a dataclass is frozen."""
    return is_dataclass(cls) and hasattr(cls, "__dataclass_params__") and getattr(cls.__dataclass_params__, "frozen", False)

def convert_dict_to_dataclass(data: dict, cls: T) -> T:
    """Convert a dictionary to a dataclass instance."""
    if not data:
        raise ValueError("Empty data dictionary")
        
    if issubclass(cls, BaseModel):
        # // 杂鱼♡～Pydantic V2 不应该再使用 parse_obj 喵，而是使用 model_validate 喵～
        if hasattr(cls, "model_validate"):
            return cls.model_validate(data)
        else:
            return cls.parse_obj(data)
    
    # // 杂鱼♡～如果是frozen dataclass，本喵就使用构造函数来创建实例，而不是先创建再赋值喵～
    if is_frozen_dataclass(cls):
        init_kwargs = {}
        t_hints = get_cached_type_hints(cls)
        
        for key, value in data.items():
            if key in t_hints:
                e_type = t_hints.get(key)
                if e_type is not None:
                    init_kwargs[key] = convert_value(key, value, e_type)
            else:
                raise ValueError(f'Unknown data key: {key}')
        
        return cls(**init_kwargs)
    else:
        # 普通dataclass可以用更高效的实例创建方式
        root_obj = cls()
        t_hints = get_cached_type_hints(cls)
        
        for key, value in data.items():
            if hasattr(root_obj, key):
                e_type = t_hints.get(key)
                if e_type is not None:
                    setattr(root_obj, key, convert_value(key, value, e_type))
            else:
                raise ValueError(f'Unknown data key: {key}')
        
        return root_obj

def convert_dataclass_to_dict(obj: Any) -> Any:
    """Convert a dataclass instance to a dictionary."""
    if obj is None:
        return None
    
    if isinstance(obj, BaseModel):
        # // 杂鱼♡～Pydantic V2 用 model_dump() 喵～不是 dict() 喵～
        if hasattr(obj, "model_dump"):
            return obj.model_dump()
        else:
            return obj.dict()
    elif isinstance(obj, Enum):
        return obj.name
    # // 杂鱼♡～本喵在这里加了一个 elif，如果遇到 set，就把它变成 list 喵！～
    elif isinstance(obj, set):
        return [convert_dataclass_to_dict(item) for item in list(obj)] # // 杂鱼♡～要递归转换 set 里面的元素喵～
    elif isinstance(obj, list):
        return [convert_dataclass_to_dict(item) for item in obj]
    elif isinstance(obj, dict):
        return {k: convert_dataclass_to_dict(v) for k, v in obj.items()}
    elif is_dataclass(obj):
        result = {}
        t_hints = get_cached_type_hints(type(obj))
        for key, value in vars(obj).items():
            e_type = t_hints.get(key)
            if e_type is not None:
                validate_type(key, value, e_type)
            result[key] = convert_dataclass_to_dict(value)
        return result
    return obj 