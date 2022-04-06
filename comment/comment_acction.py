import sqlite3
from comment import comment_model


class CommentAcction:
    def __init__(self, db_connection) -> None:
        self.db_connection = db_connection

    def show_all(self):
        conn = sqlite3.connect(self.db_connection)
        cur = conn.cursor()
        sql = "SELECT * FROM comment "
        cur.execute(sql)
        rows = cur.fetchall()
        result = []
        for row in rows:
            Comment = comment_model.Comment(
                comment_ID=row[0],
                detail=row[1],
                username=row[2],
                time=row[3],
                post_ID=row[4],
                point=row[5]
            )
            result.append(Comment.visibale())
        return result

    def showbyID(self, id):
        conn = sqlite3.connect(self.db_connection)
        cur = conn.cursor()
        sql = "SELECT * FROM comment WHERE post_ID='"+str(id)+"'"
        cur.execute(sql)
        rows = cur.fetchall()
        result = []
        for row in rows:
            Comment = comment_model.Comment(
                comment_ID=row[0],
                detail=row[1],
                username=row[2],
                time=row[3],
                post_ID=row[4],
                point=row[5]
            )
            result.append(Comment.visibale())
        return result
