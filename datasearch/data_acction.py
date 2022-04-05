import sqlite3
from datasearch import data_model

class DataAcction:
    def __init__(self, db_connection) -> None:
        self.db_connection = db_connection

    def getall(self):
        conn = sqlite3.connect(self.db_connection)
        cur = conn.cursor()
        sql = "SELECT * FROM searchdata"
        cur.execute(sql)
        rows = cur.fetchall()
        result = []
        for row in rows:
            DataModel = data_model.DataModel(
                id = row[0],
                detail=row[1],
                username=row[2],
                count=row[3],
            )
            result.append(DataModel.visibale())
        return result