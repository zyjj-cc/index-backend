import hashlib
from dataclasses import fields, MISSING
from zoneinfo import ZoneInfo

from surrealdb import RecordID
from datetime import datetime

def get_datetime_now():
    """获取当时时间"""
    return datetime.now(tz=ZoneInfo('Asia/Shanghai'))

def init_dataclass_from_dict(dataclass_cls, data_dict):
    """
    从dict初始化dataclass对象
    :param dataclass_cls:  dataclass对象
    :param data_dict: 数据字典
    :return:
    """
    init_kwargs = {}
    if not data_dict:
        raise Exception("data is none")
    for field in fields(dataclass_cls):
        name = field.name
        if name in data_dict:
            value = data_dict[name]
            if isinstance(value, RecordID):
                value = value.id
            init_kwargs[name] = value
        elif field.default is MISSING:
            raise Exception(f"{name} is required")
    return dataclass_cls(**init_kwargs)

def dataclass_to_dict(dataclass_cls) -> dict:
    """
    从dict初始化dataclass对象
    :param dataclass_cls:  dataclass对象
    :return:
    """
    data = dataclass_cls.__dict__
    for k, v in data.items():
        if isinstance(v, datetime):
            data[k] = int(v.timestamp()*1000)

    return data

def calculate_md5(byte_data):
    """
    计算文件的md5值
    :param byte_data: 文件数据
    :return:
    """
    # 创建 MD5 哈希对象
    md5_hash = hashlib.md5()
    # 更新哈希对象内容
    md5_hash.update(byte_data)
    # 获取十六进制格式的哈希值
    return md5_hash.hexdigest()