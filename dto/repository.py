import sqlite3
import pathlib
from model.user import User
from model.record import Record


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

    def add_user(self, phone_number, full_name, password):
        self.open_connection()
        self.cursor.execute("INSERT INTO users VALUES (?, ?, 'CLIENT', ?)",
                            phone_number, full_name, password)
        self.close_connection()

    def find_user(self, phone_number) -> User:
        self.open_connection()
        self.cursor.execute("SELECT * FROM users WHERE phone_number = ?", phone_number)
        res = self.cursor.fetchone()
        self.close_connection()

        if len(res) == 0:
            return None

        phone = res[0]
        name = res[1]
        u_type = res[2]
        password = res[3]
        return User(phone, name, password, u_type)

    def add_record(self, time_start, comment, user_id):
        self.open_connection()
        self.cursor.execute("INSERT INTO records VALUES (?, ?)",
                            time_start, comment)
        record_id = self.cursor.lastrowid
        self.cursor.execute("INSERT INTO user_records VALUES (?, ?)",
                            user_id, record_id)
        self.close_connection()

    def find_records_by_user(self, user_id) -> List[Record]:
        self.open_connection()
        self.cursor.execute("""
            SELECT r.* FROM user_records AS ur 
            INNER JOIN records r ON ur.record_id = r.id 
            WHERE ur.user_id = ?
        """, user_id)
        res = self.cursor.fetchall()
        self.close_connection()
        records = []
        for record in res:
            rec_id = record[0]
            rec_time = record[1]
            rec_comm = record[2]
            r = Record(rec_id, rec_time, rec_comm)
            records.append(r)
        return records

    def update_record(self, id, time, comment) -> Record:
        self.open_connection()
        self.cursor.execute("""
            UPDATE records 
            SET time_start = ?,
                comment = ?
            WHERE id = ?
        """, time, comment, id)
        self.close_connection()
        return Record(id, time, comment)

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
            
            INSERT INTO users VALUES ('admin', 'admin', 'ADMIN', 'ya_sobaka');
            
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
