from dataclasses import dataclass
from datetime import datetime


@dataclass
class EntityInfo:
    name: str
    id: str = ''
    entity_type: int = 0
    data: dict = None
    create_time: datetime = None


@dataclass
class FileInfo:
    id: str
    name: str
    size: int
    md5: str
    create_time: datetime

