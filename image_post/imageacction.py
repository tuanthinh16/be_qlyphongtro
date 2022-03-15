import sqlite3
from image_post import imagemodel

class ImagePostAction:
    def __init__(self, db_connection) -> None:
        self.db_connection = db_connection
    def getimage(self,id):
        conn = sqlite3.connect(self.db_connection)
        cur = conn.cursor()
        sql = "SELECT * FROM image_save WHERE post_id='"+str(id)+"'"
        cur.execute(sql)
        rows = cur.fetchall()
        result = []
        for row in rows:
            ImagePost = imagemodel.ImagePost(
                image_id=row[0],
                name_file=row[1],
                post_id=row[2],
                img=row[3]
            )
            result.append(ImagePost.visibale())
        return result
