from turtle import pos
from flask import Flask, json
from flask import jsonify
from flask_cors import CORS
from flask import Flask, redirect, request, render_template, session, flash
import datetime
import sqlite3
import time
from werkzeug.utils import secure_filename
import os.path
from PIL import Image
from io import BytesIO
from flask import send_file, send_from_directory
from flask import Response
import io
import zipfile
from os.path import basename
import os


from comment.comment_acction import CommentAcction
from post.post_acction import PostAcction
from account.account_acction import AccountAcction
from image_post.imageacction import ImagePostAction

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origin": "*"}})
connection_data = ('phongtro.db')


@app.route('/api/')
def index():
    return ("hello")

@app.route('/api/resigter', methods=['POST'])
def resigter():
    name = request.form['name']
    username = request.form['username']
    password = request.form['password']
    repassword = request.form['repassword']
    email = request.form['email']
    phone = request.form['phone']
    con = sqlite3.connect(connection_data)
    cur = con.cursor()
    isRecordExit = 0
    rows = cur.execute(
        "SELECT * FROM user WHERE username ='"+str(username)+"'")
    for row in rows:
        isRecordExit = 1
    if isRecordExit == 1:
        return "Account has been exited", 401
    else:
        if(password == repassword):
            sql = "INSERT INTO user('name','username','password','email','phone') VALUES ('"+str(name) + \
                "','"+str(username)+"','"+str(password) + \
                "','"+str(email)+"','"+str(phone)+"')"
            cur.execute(sql)
            con.commit()
            con.close()
        else:
            return "Invalid", 401
    return "thanh cong", 200


@app.route('/api/login', methods=['POST'])
def login():
    username = request.form["username"]
    password = request.form["password"]
    print(username, password)
    conn = sqlite3.connect(connection_data)
    cur = conn.cursor()
    isRecordExit = 0
    sql = "SELECT * FROM user WHERE username ='"+str(username)+"'"
    cur.execute(sql)
    for row in cur:
        isRecordExit = 1
    if isRecordExit == 1:
        if str(row[2]) == username and str(row[3]) == password:
            if str(row[6]) == '0':
                return "admin login", 200
            else:
                return "user login", 200
        else:
            return "error", 401
    else:
        print(" tai khoan khong ton tai")
        return "khong ton tai", 401
    return redirect('/api/')

@app.route('/api/getname/<string:usr>')
def getfullname(usr):
    Account = AccountAcction(connection_data)
    return jsonify(Account.showname(usr))
    
@app.route('/api/getalluser')
def getalluser():
    Account = AccountAcction(connection_data)
    return jsonify(Account.showall())


@app.route('/api/sigout')
def sigout():
    session.pop("username", None)
    flash("You have been log out !!")
    return redirect('/api/login')


@app.route('/api/addcmt', methods=['POST'])
def addcomment():
    detail = request.form["comment"]
    username = request.form["username"]
    time = datetime.datetime.now()
    post_ID = request.form["post_ID"]
    conn = sqlite3.connect(connection_data)
    cur = conn.cursor()
    sql = "INSERT INTO comment('detail','username','time','post_ID') VALUES('" + \
        str(detail)+"','"+str(username)+"','" + \
        str(time)+"'," + post_ID+")"
    cur.execute(sql)
    conn.commit()
    conn.close()
    return "thanh cong", 200


@ app.route('/api/showcomment')
def showcommet():
    Comment = CommentAcction(connection_data)
    result = Comment.show_all()
    return jsonify(result)

 
@app.route('/api/showcmtbyID/<int:id>')
def showcmtbyID(id):
    Comment = CommentAcction(connection_data)
    result = Comment.showbyID(id)
    return jsonify(result)


@app.route('/api/getidimage/<int:id>')
def getidimage(id):
    con = sqlite3.connect(connection_data)
    cur = con.cursor()
    sql = "SELECT * FROM image_save WHERE post_id='"+str(id)+"'"
    cur.execute(sql)
    rows = cur.fetchall()
    images = []
    for row in rows:
        image_id = row[0]
        name_file = row[1]
        post_id = row[2]
        img = row[3]
        write_file(img, name_file, post_id)
        images.append(image_id)
        #print("size file:", (img))
    return jsonify(
        {
            'id_image': images,
        })


@app.route("/api/getimage/<int:id>")
def getimage(id):
    con = sqlite3.connect(connection_data)
    cur = con.cursor()
    sql = "SELECT * FROM image_save WHERE image_id='"+str(id)+"'"
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
        image_id = row[0]
        name_file = row[1]
        post_id = row[2]
        img = row[3]
    return send_file(BytesIO(img), mimetype='image/jpeg', attachment_filename=name_file)


def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file),
                       os.path.relpath(os.path.join(root, file),
                                       os.path.join(path, '..')))


def write_file(data, filename, idf):
    if not os.path.exists("images\\"+idf+"\\"):
        os.makedirs("images\\"+idf+"\\")
    with open("images\\"+idf+"\\"+filename, 'wb') as f:
        f.write(data)


@app.route('/api/addimage', methods=['POST'])
def addimage():
    ids = request.form['ids']
    print("ids: "+ids)
    image = request.files['files']
    con = sqlite3.connect(connection_data)
    cur = con.cursor()
    img = image.read()
    # for i in range(len(image)):
    #     print("image: "+image[i])
    filename = secure_filename(image.filename)
    #img.save("./images/", filename)
    # image.save(os.path.join('../images', filename))
    sql2 = """INSERT INTO image_save('name_file','img','post_ID') VALUES (?,?,?)"""

    data_tuple = (filename, img, ids)
    cur.execute(sql2, data_tuple)
    con.commit()
    con.close()
    return jsonify({
        'success': True,
        'file': 'Received'
    })


@app.route('/api/addpost', methods=['POST'])
def addpost():
    ids = request.form['ids']
    loai = ''
    title = request.form['title']
    types = request.form['type']
    # print("File"+request.files['files'])
    if types == 'thue':
        loai = 'Cho Thuê'
    elif types == 'tim':
        loai = 'Tìm Phòng'
    elif types == 'ghep':
        loai = 'Ở Ghép'
    elif types == 'homestay':
        loai = 'Căn Hộ'
    elif types == 'other':
        loai = 'Khác'
    dientich = request.form['dientich']
    diachi = request.form['diachi']
    detail = request.form['detail']
    username = request.form['username']
    cost = request.form['cost']
    time_posted = datetime.datetime.now()

    con = sqlite3.connect(connection_data)
    cur = con.cursor()
    sql = "INSERT INTO post ('post_ID','title', 'type','dientich','address', 'detail', 'username','timeposted','cost') VALUES ('"+str(ids)+"','"+str(
        title)+"','"+str(loai)+"','"+str(dientich)+"','"+str(diachi)+"','"+str(detail)+"','"+str(username)+"','"+str(time_posted)+"','"+str(cost)+"')"
    cur.execute(sql)
    con.commit()
    con.close()
    return "thanh cong", 200


@app.route('/api/showpost')
def showpost():
    Posts = PostAcction(connection_data)
    rs = Posts.show_all()
    return jsonify(rs)


@app.route('/api/deletepost/<int:id>')
def deletepost(id):
    conn = sqlite3.connect(connection_data)
    cur = conn.cursor()
    sql = "DELETE FROM post WHERE post_ID='"+str(id)+"'"
    cur.execute(sql)
    conn.commit()
    conn.close()
    return "thanh cong", 200


@app.route('/api/selectpost/<int:id>')
def selectpostById(id):
    Posts = PostAcction(connection_data)
    result = Posts.showById(id)
    return jsonify(result)


@app.route('/api/editpost', methods=['POST'])
def editpostById():
    post_ID = request.form['post_ID']
    title = request.form['title']
    type = request.form['type']
    detail = request.form['detail']
    conn = sqlite3.connect(connection_data)
    cur = conn.cursor()
    sql = "UPDATE post SET title='" + \
        str(title)+"', type='"+str(type)+"', detail='" + \
        str(detail)+"' WHERE post_ID = "+post_ID
    cur.execute(sql)
    conn.commit()
    conn.close()
    return "thanh cong", 200


@app.route("/api/showbytype/<int:id>")
def showbyType(id):
    if id == 1:
        type = 'Cho Thuê'
    elif id == 2:
        type = 'Tìm Phòng'
    elif id == 3:
        type = 'Ở Ghép'
    elif id == 4:
        type = 'Căn Hộ'
    elif id == 5:
        type = 'Khác'
    Posts = PostAcction(connection_data)
    result = Posts.showbytype(type)
    return jsonify(result)


@app.route('/api/deletecomment/<int:id>')
def delete(id):
    conn = sqlite3.connect(connection_data)
    cur = conn.cursor()
    sql = "DELETE FROM comment WHERE comment_ID='"+str(id)+"'"
    cur.execute(sql)
    conn.commit()
    conn.close()
    return "thanh cong", 200

@app.route('/api/adddataaSearch',methods=['POST'])
def adddata():
    value = request.form['value']
    username = request.form['username']
    conn = sqlite3.connect(connection_data)
    cur = conn.cursor()
    sql = "INSERT INTO searchdata('detail','username') VALUES ('"+str(value)+"','"+str(username)+"')"
    cur.execute(sql)
    conn.commit()
    conn.close()
    return "ok",200
@app.route('/api/search/<string:value>')
def search(value):
    Posts = PostAcction(connection_data)
    rs = Posts.search(value)
    return jsonify(rs)


@app.route('/api/report/<int:id>')
def report(id):
    print("id report: "+str(id))
    return "thanh cong ", 200


@app.route('/api/like/<int:id>')
def like(id):
    conn = sqlite3.connect(connection_data)
    cur = conn.cursor()
    cur.execute("SELECT * FROM comment WHERE comment_ID='"+str(id)+"'")
    for row in cur:
        point = int(row[5])
        point += 1
    cur.execute("UPDATE comment SET point ='"+str(point) +
                "' WHERE comment_ID='"+str(id)+"'")
    conn.commit()
    conn.close()
    return "ok", 200


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['TESTING'] = True
    app.testing = True
    app.run(host='0.0.0.0', port=5000, debug=True)
