"""杂鱼♡～这是本喵为你写的dataclass到JSON的序列化函数喵～才不是特意为了杂鱼写的呢～"""

import os
from typing import Any
from dataclasses import is_dataclass
from pydantic import BaseModel

from .core import T, convert_dataclass_to_dict
from .file_ops import ensure_directory_exists, save_json_file

def jsdc_dump(obj: T, output_path: str, encoding: str = 'utf-8', indent: int = 4) -> None:
    """杂鱼♡～本喵帮你把dataclass或Pydantic模型实例序列化成JSON文件喵～

    这个函数接收一个dataclass实例，并将其序列化表示写入到指定文件中，
    格式为JSON喵～输出文件可以使用指定的字符编码，JSON输出可以
    使用指定的缩进级别格式化喵～杂鱼一定会感激本喵的帮助的吧♡～

    Args:
        obj (T): 要序列化的dataclass实例喵～
        output_path (str): 要保存JSON数据的输出文件路径喵～杂鱼可别搞错路径哦～
        encoding (str, optional): 输出文件使用的字符编码喵～默认是'utf-8'～
        indent (int, optional): JSON输出中使用的缩进空格数喵～默认是4～看起来整齐一点～

    Raises:
        ValueError: 如果提供的对象不是dataclass或路径无效，本喵会生气地抛出错误喵！～
        TypeError: 如果obj不是dataclass或BaseModel，杂鱼肯定传错参数了～
        OSError: 如果遇到文件系统相关错误，杂鱼的硬盘可能有问题喵～
        UnicodeEncodeError: 如果编码失败，杂鱼选的编码有问题喵！～
    """
    if not output_path or not isinstance(output_path, str):
        raise ValueError("杂鱼♡～输出路径无效喵！～")
    
    if indent < 0:
        raise ValueError("杂鱼♡～缩进必须是非负数喵！～负数是什么意思啦～")

    try:
        # 确保目录存在且可写喵～
        directory = os.path.dirname(os.path.abspath(output_path))
        ensure_directory_exists(directory)

        if isinstance(obj, type):
            raise TypeError("杂鱼♡～obj必须是实例而不是类喵！～你真是搞不清楚呢～")
            
        if not (is_dataclass(obj) or isinstance(obj, BaseModel)):
            raise TypeError('杂鱼♡～obj必须是dataclass或Pydantic BaseModel实例喵！～')
            
        data_dict = convert_dataclass_to_dict(obj)
        save_json_file(output_path, data_dict, encoding, indent)
    except OSError as e:
        raise OSError(f"杂鱼♡～创建目录或访问文件失败喵：{str(e)}～")
    except TypeError as e:
        raise TypeError(f"杂鱼♡～类型验证失败喵：{str(e)}～真是个笨蛋呢～")
    except Exception as e:
        raise ValueError(f"杂鱼♡～序列化过程中出错喵：{str(e)}～") 