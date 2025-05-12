from dataclasses import dataclass
from datetime import datetime


@dataclass
class EntityInfo:
    name: str  # 实体名称
    entity_type: int = 0  # 实体类型
    id: str = ''  # 实体id
    data: dict = None  # 实体数据
    create_time: datetime = None  # 实体创建时间
    update_time: datetime = None  # 实体更新时间


@dataclass
class EntityRelation:
    source: str  # 源节点id
    target: str  # 目标节点id
    relation_type: int = 0  # 关联类型
    data: dict = None
    create_time: datetime = None


@dataclass
class FileInfo:
    id: str  # 文件id
    name: str  # 文件名称
    content_type: str  # 文件类型
    size: int  # 文件大小
    md5: str  # 文件md5值
    create_time: datetime  # 文件创建时间
