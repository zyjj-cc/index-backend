from core.entity import EntityService
from core.file import FileService

from infra import Db, Data


class Api:
    def __init__(self, db: Db, data: Data):
        self.entity = EntityService(db)
        self.file = FileService(db, data)

