import datetime

class Logger:

    def __init__(self, db):
        self.db = db

    def log(self, src, dst, text):
        self.db.cursor.execute(
            "INSERT INTO logs VALUES (?, ?, ?, ?);",
                (str(datetime.datetime.now().time()),
                src,
                dst,
                text,))
        self.db.commit()
