import sqlite3
import pathlib
from model.user import User


class DB:
    def __init__(self) -> None:
        self.cursor = None
        self.conn = None
        try:
            self.path = pathlib.Path().absolute() / "db_files" / "main.db"
            self.open_connection()
            self.migration()
        except sqlite3.Error as error:
            print(error)
        finally:
            if self.conn:
                self.close_connection()

    def find_user(self, phone_number):
        self.open_connection()
        self.cursor.execute(f"""
            SELECT * FROM users WHERE phone_number = '{phone_number}'
        """)
        res = self.cursor.fetchone()
        self.close_connection()

        if len(res) == 0:
            return None

        phone = res[0]
        name = res[1]
        u_type = res[2]
        password = res[3]
        return User(phone, name, password, u_type)

    def open_connection(self):
        self.conn = sqlite3.connect(self.path)
        self.cursor = self.conn.cursor()

    def close_connection(self):
        self.conn.close()

    def migration(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS IF NOT EXISTS users(
                phone_number TEXT PRIMARY KEY,
                full_name TEXT NOT NULL,
                type INTEGER NOT NULL,
                password TEXT NOT NULL
            );
            
            CREATE TABLE IF NOT EXISTS records(
                id INTEGER PRIMARY KEY,
                time_start INTEGER NOT NULL,
                comment TEXT,
            );
            
            CREATE TABLE IF NOT EXISTS user_records(
               id INTEGER PRIMARY KEY,
               user_id INTEGER NOT NULL,
               record_id INTEGER NOT NULL,
               FOREIGN KEY(user_id) REFERENCES users(id),
               FOREIGN KEY(record_id) REFERENCES records(id),
            );
        ''')
