import sqlite3

class DB:
    def __init__(self, db_path):
        self._conn = sqlite3.connect(db_path)
        self.cursor = self._conn.cursor()

        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS logs (
                date DATETIME,
                src VARCHAR(255),
                dst VARCHAR(255),
                message TEXT
            );""")

    def commit(self):
        self._conn.commit()

    def close(self):
        self._conn.close()
