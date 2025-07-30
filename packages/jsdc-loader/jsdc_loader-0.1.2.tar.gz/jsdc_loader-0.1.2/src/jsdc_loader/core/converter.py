"""Conversion utilities for JSDC Loader."""

from typing import Any, Type, get_args, get_origin, Union
from dataclasses import is_dataclass
from enum import Enum
from pydantic import BaseModel
import datetime
import uuid
from decimal import Decimal

from .types import T
from .validator import get_cached_type_hints

def convert_enum(key: str, value: Any, enum_type: Type[Enum]) -> Enum:
    """Convert a string value to an Enum member."""
    try:
        return enum_type[value]
    except KeyError:
        raise ValueError(f'Invalid Enum value for key {key}: {value}')

def convert_union_type(key: str, value: Any, union_type: Any) -> Any:
    """Convert a value to one of the Union types."""
    args = get_args(union_type)
    
    # 杂鱼♡～处理None值喵～
    if value is None and type(None) in args:
        return None
        
    # 尝试所有可能的类型转换，直到成功喵～
    for arg_type in args:
        if arg_type is type(None):
            continue
            
        try:
            return convert_value(key, value, arg_type)
        except (ValueError, TypeError):
            continue
            
    # 如果所有转换都失败，则抛出错误喵～
    raise TypeError(f'杂鱼♡～无法将键{key}的值{value}转换为{union_type}喵！～')

def convert_simple_type(key: str, value: Any, e_type: Any) -> Any:
    """Convert a value to a simple type."""
    # 杂鱼♡～处理特殊类型喵～
    if e_type is Any:
        return value
    elif isinstance(e_type, type) and issubclass(e_type, Enum):
        return e_type[value]
    elif e_type == dict or get_origin(e_type) == dict:
        # Handle dict type properly
        return value
    elif e_type == list or get_origin(e_type) == list:
        # Handle list type properly
        return value
    # 杂鱼♡～处理复杂类型喵～如日期、时间等
    elif e_type == datetime.datetime and isinstance(value, str):
        return datetime.datetime.fromisoformat(value)
    elif e_type == datetime.date and isinstance(value, str):
        return datetime.date.fromisoformat(value)
    elif e_type == datetime.time and isinstance(value, str):
        return datetime.time.fromisoformat(value)
    elif e_type == datetime.timedelta and isinstance(value, (int, float)):
        return datetime.timedelta(seconds=value)
    elif e_type == datetime.timedelta and isinstance(value, dict):
        return datetime.timedelta(**value)
    elif e_type == uuid.UUID and isinstance(value, str):
        return uuid.UUID(value)
    elif e_type == Decimal and isinstance(value, (str, int, float)):
        return Decimal(str(value))
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

def convert_tuple_type(key: str, value: list, e_type: Any) -> tuple:
    """杂鱼♡～本喵帮你把列表转换成元组喵～"""
    if get_origin(e_type) is tuple:
        args = get_args(e_type)
        if len(args) == 2 and args[1] is Ellipsis:  # Tuple[X, ...]
            element_type = args[0]
            return tuple(convert_value(f"{key}[{i}]", item, element_type) for i, item in enumerate(value))
        elif args:  # Tuple[X, Y, Z]
            if len(value) != len(args):
                raise ValueError(f"杂鱼♡～元组{key}的长度不匹配喵！期望{len(args)}，得到{len(value)}～")
            return tuple(convert_value(f"{key}[{i}]", item, arg_type) 
                        for i, (item, arg_type) in enumerate(zip(value, args)))
    
    # 如果没有参数类型或者其他情况，直接转换为元组喵～
    return tuple(value)

def convert_value(key: str, value: Any, e_type: Any) -> Any:
    """Convert a value to the expected type."""
    # 杂鱼♡～处理None值和Any类型喵～
    if value is None and (e_type is Any or (get_origin(e_type) is Union and type(None) in get_args(e_type))):
        return None
    
    # 杂鱼♡～如果期望类型是Any，直接返回值喵～
    if e_type is Any:
        return value
    
    # // 杂鱼♡～本喵在这里加了一段逻辑，如果期望的是 set 但得到的是 list，就把它转成 set 喵！～
    if (get_origin(e_type) is set or e_type is set) and isinstance(value, list):
        args = get_args(e_type)
        if args: # // 杂鱼♡～如果 set 里面有类型定义，比如 Set[Model]，那就要对每个元素进行转换喵～
            element_type = args[0]
            return {convert_value(f"{key}[*]", item, element_type) for item in value}
        else: # // 杂鱼♡～如果只是普通的 set，比如 Set[str]，就直接转喵～
            return set(value)
            
    # 杂鱼♡～处理元组类型喵～
    if (get_origin(e_type) is tuple or e_type is tuple) and isinstance(value, list):
        return convert_tuple_type(key, value, e_type)

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
    
    # 杂鱼♡～处理特殊类型喵～
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    elif isinstance(obj, datetime.date):
        return obj.isoformat()
    elif isinstance(obj, datetime.time):
        return obj.isoformat()
    elif isinstance(obj, datetime.timedelta):
        return obj.total_seconds()
    elif isinstance(obj, uuid.UUID):
        return str(obj)
    elif isinstance(obj, Decimal):
        return str(obj)
    elif isinstance(obj, tuple):
        return [convert_dataclass_to_dict(item) for item in obj]
    
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
            # 杂鱼♡～这里我们不再使用validate_type来验证，因为我们只是要将值转换为字典喵～
            result[key] = convert_dataclass_to_dict(value)
        return result
    return obj 