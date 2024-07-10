from src.database.init import init_db, get_db, SessionLocal


class Database():
    def __init__(self):
        init_db()
        get_db()

    def get_session(self):
        return SessionLocal()
