from dto.repository import DB


class UserService:

    def __init__(self, db: DB):
        self.db = db
