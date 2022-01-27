from dto.repository import DB


class RecordService:

    def __init__(self, db: DB):
        self.db = db
