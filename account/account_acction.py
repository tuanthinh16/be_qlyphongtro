import sqlite3
from account import account_model


class AccountAcction:
    def __init__(self, db_connection) -> None:
        self.db_connection = db_connection

    def showall(self):
        conn = sqlite3.connect(self.db_connection)
        cur = conn.cursor()
        sql = "SELECT * FROM user"
        cur.execute(sql)
        rows = cur.fetchall()
        result = []
        for row in rows:
            account = account_model.Account(
                name=row[1],
                username=row[2],
                password=row[3],
                email=row[4],
                phone=row[5],
                role=row[6]
            )
            result.append(account.visibale())
        return result
