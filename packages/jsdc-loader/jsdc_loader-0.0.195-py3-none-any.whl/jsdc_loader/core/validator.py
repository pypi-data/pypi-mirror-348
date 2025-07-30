"""杂鱼♡～这是本喵的验证工具喵～本喵可是非常严格的，不会让杂鱼传入错误的类型呢～"""

from typing import Any, get_args, get_origin, Union, Type, Dict
from dataclasses import is_dataclass
from enum import Enum
from pydantic import BaseModel
import functools

from .types import _TYPE_HINTS_CACHE

def get_cached_type_hints(cls: Type) -> Dict[str, Any]:
    """杂鱼♡～本喵用缓存来获取类型提示，这样速度更快喵～"""
    if cls not in _TYPE_HINTS_CACHE:
        from typing import get_type_hints
        _TYPE_HINTS_CACHE[cls] = get_type_hints(cls)
    return _TYPE_HINTS_CACHE[cls]

def validate_dataclass(cls: Any) -> None:
    """杂鱼♡～本喵帮你验证提供的类是否为dataclass或BaseModel喵～杂鱼总是分不清这些～"""
    if not cls:
        raise TypeError("杂鱼♡～data_class不能为None喵！～")
    if not (is_dataclass(cls) or issubclass(cls, BaseModel)):
        raise TypeError('杂鱼♡～data_class必须是dataclass或Pydantic BaseModel喵！～')

def validate_type(key: str, value: Any, e_type: Any) -> None:
    """杂鱼♡～本喵帮你验证值是否匹配预期类型喵～本喵很擅长发现杂鱼的类型错误哦～"""
    o_type = get_origin(e_type)
    if o_type is Union:
        if value is not None and not any(isinstance(value, t) for t in get_args(e_type) if t is not type(None)):
            raise TypeError(f'杂鱼♡～键{key}的类型无效喵：期望{e_type}，得到{type(value)}～你连类型都搞不清楚吗？～')
    elif o_type is not None:
        if not isinstance(value, o_type):
            raise TypeError(f'杂鱼♡～键{key}的类型无效喵：期望{o_type}，得到{type(value)}～真是个笨蛋呢～')
    else:
        if not isinstance(value, e_type):
            raise TypeError(f'杂鱼♡～键{key}的类型无效喵：期望{e_type}，得到{type(value)}～') 