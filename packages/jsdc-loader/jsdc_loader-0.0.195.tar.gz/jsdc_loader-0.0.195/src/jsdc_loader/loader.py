"""杂鱼♡～这是本喵为你写的JSON到dataclass的反序列化函数喵～"""

import json
import os
from typing import Union, TextIO, Any

from .core import T, validate_dataclass, convert_dict_to_dataclass
from .file_ops import check_file_size

def jsdc_load(fp: Union[str, TextIO], data_class: T, encoding: str = 'utf-8', max_size: int = 10 * 1024 * 1024) -> T:
    """
    杂鱼♡～本喵帮你把JSON文件反序列化成dataclass对象喵～

    :param fp: 可以是文件路径或者支持.read()的文件对象喵～杂鱼知道这是什么意思吗？～
    :param data_class: 要反序列化成的dataclass类型喵♡～本喵可以处理任何复杂类型哦～
    :param encoding: 文件编码格式，默认是utf-8喵～杂鱼应该不需要改这个～
    :param max_size: 最大允许的文件大小（字节），默认10MB喵～太大了本喵会生气的哦♡～
    :return: data_class类型的实例喵～
    :raises: ValueError：如果文件太大或路径无效时，本喵会抛出这个错误喵～
    :raises: FileNotFoundError：找不到文件时，杂鱼是不是搞错路径了？～
    :raises: PermissionError：没有权限访问文件时，杂鱼♡需要提升权限喵～
    :raises: JSONDecodeError：JSON格式错误时，杂鱼写的JSON有问题喵！～
    """
    if isinstance(fp, str):
        if not fp or not isinstance(fp, str):
            raise ValueError("杂鱼♡～文件路径无效喵！～")
        
        try:
            check_file_size(fp, max_size)
            
            with open(fp, 'r', encoding=encoding) as f:
                return jsdc_loads(f.read(), data_class)
        except FileNotFoundError:
            raise FileNotFoundError(f"杂鱼♡～找不到文件喵：{fp}～肯定是杂鱼把路径搞错了喵！～")
        except PermissionError:
            raise PermissionError(f"杂鱼♡～没有权限访问文件喵：{fp}～需要提升权限才行喵～")
        except UnicodeDecodeError:
            raise ValueError(f"杂鱼♡～文件编码错误喵！～应该使用{encoding}编码的说～")
    else:
        try:
            content = fp.read()
            if len(content.encode('utf-8')) > max_size:
                raise ValueError(f"杂鱼♡～内容太大了喵～超过了{max_size}字节的限制～本喵处理不了那么大的内容啦～")
            return jsdc_loads(content, data_class)
        except Exception as e:
            raise ValueError(f"杂鱼♡～读取文件对象时出错喵：{str(e)}～真是个笨蛋呢～")

def jsdc_loads(s: str, data_class: T) -> T:
    """
    杂鱼♡～本喵帮你把JSON字符串反序列化成dataclass对象喵～

    :param s: 含有JSON数据的字符串喵～
    :param data_class: 要反序列化成的dataclass类型喵♡～
    :return: data_class类型的实例喵～
    :raises: ValueError：如果输入无效或类型不匹配，本喵会生气地抛出这个错误喵～
    :raises: TypeError：如果data_class不是有效的dataclass或BaseModel，杂鱼是不是传错类型了？～
    :raises: JSONDecodeError：JSON格式错误时，杂鱼写的JSON有问题喵！～
    """
    if not isinstance(s, str):
        raise ValueError("杂鱼♡～输入必须是字符串喵！～")
    
    if not s.strip():
        raise ValueError("杂鱼♡～输入字符串是空的或只有空白符喵！～")

    try:
        data = json.loads(s)
        if not isinstance(data, dict):
            raise ValueError("杂鱼♡～JSON根必须是对象类型喵！～")
        
        validate_dataclass(data_class)
        return convert_dict_to_dataclass(data, data_class)
    except json.JSONDecodeError as e:
        raise ValueError(f"杂鱼♡～JSON格式无效喵：{str(e)}～")
    except Exception as e:
        raise ValueError(f"杂鱼♡～反序列化时出错喵：{str(e)}～") 