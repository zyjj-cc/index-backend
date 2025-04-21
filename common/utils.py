import hashlib
from dataclasses import fields
from surrealdb import RecordID


def init_dataclass_from_dict(dataclass_cls, data_dict):
    """
    从dict初始化dataclass对象
    :param dataclass_cls:  dataclass对象
    :param data_dict: 数据字典
    :return:
    """
    field_names = [field.name for field in fields(dataclass_cls)]
    init_kwargs = {}
    for name in field_names:
        if name in data_dict:
            value = data_dict[name]
            if isinstance(value, RecordID):
                value = value.id
            init_kwargs[name] = value
    return dataclass_cls(**init_kwargs)

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