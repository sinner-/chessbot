import datetime

class Logger:
    def __init__(self, db):
        self._db = db

    def log(self, src, dst, text):
        self._db.cursor.execute(
            "INSERT INTO logs VALUES (?, ?, ?, ?);", (
                str(datetime.datetime.now().time()),
                src,
                dst,
                text,
            )
        )
        self._db.commit()
