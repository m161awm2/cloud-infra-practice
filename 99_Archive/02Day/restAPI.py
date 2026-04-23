# REST API FLIE
from flask import Flask,render_template,request,session,jsonify
import pymysql
from DB_password import DB_ENDPOINT,DB_PASSWORD

app = Flask(__name__)
app.secret_key = DB_PASSWORD

def makeDb():
    conn = pymysql.connect(
        host=DB_ENDPOINT,
        user="root",
        passwd=DB_PASSWORD,
    )
    c = conn.cursor()
    c.execute("CREATE DATABASE IF NOT EXISTS 02Day")
    conn.commit()
    conn.close()

def get_conn():
    return pymysql.connect(
        host=DB_ENDPOINT,
        user="root",
        passwd=DB_PASSWORD,
        database="02Day",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )

def init_db():
    conn = get_conn()
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS posts(
              id INT AUTO_INCREMENT PRIMARY KEY,
              title VARCHAR(200),
              content TEXT,
              nickname TEXT
              )""")
    c.execute("""CREATE TABLE IF NOT EXISTS users(
              id INT AUTO_INCREMENT PRIMARY KEY,
              nickname VARCHAR(30),
              password TEXT
              )
              """)
    c.execute("""CREATE TABLE IF NOT EXISTS comments(
              id INT AUTO_INCREMENT PRIMARY KEY,
              nickname TEXT,
              content TEXT,
              post_id INT
              )
              """)
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template('index.html')
@app.route('/api/board',methods=["GET"])
def board():
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM posts ORDER BY id DESC")
    posts = c.fetchall()
    nickname = session.get("user")
    conn.close()
    return jsonify({
        "posts" : posts,
        "nickname" : nickname
    })

@app.route('/detail/<int:post_id>',methods=["GET"])
def detail(post_id):
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM posts WHERE id = %s",(post_id,))
    post = c.fetchone()
    conn.close()
    return render_template("detail.html",post=post)

@app.route('/write')
def get_write():
    return render_template("write.html")
@app.route('/api/write',methods=["POST"])
def write():
    nickname = session.get("user")
    if not nickname:
        return jsonify({"message" : "로그인을 먼저 해주세요!"})
    data = request.get_json()
    title = data.get("title")
    content = data.get("content")
    conn = get_conn()
    c = conn.cursor()
    c.execute("INSERT INTO posts (nickname,title,content) VALUES (%s,%s,%s)",
              (nickname,title,content))
    conn.commit()
    conn.close()
    return jsonify({"message" : "글쓰기가 완료되었습니다!"})

@app.route('/login',methods=["GET"])
def get_login():
    return render_template("login.html")
@app.route('/api/login',methods=["POST"])
def login():
    conn = get_conn()
    c = conn.cursor()
    data = request.get_json()
    nickname = data.get("nickname")
    password = data.get("password")
    c.execute("SELECT * FROM users WHERE nickname = %s AND password = %s",(nickname,password))
    is_login = c.fetchone()
    conn.close()
    if not is_login:
        return jsonify({"message" : "닉네임과 비밀번호를 다시 확인하세요!"})
    session["user"] = nickname
    return jsonify({"message" : "로그인이 완료되었습니다!"})

@app.route('/register')
def get_register():
    return render_template("register.html")
@app.route('/api/register',methods=["POST"])
def register():
    conn = get_conn()
    c = conn.cursor()
    data = request.get_json()
    nickname = data.get("nickname")
    password = data.get("password")
    c.execute("SELECT * FROM users WHERE nickname = %s",(nickname,))
    is_exists = c.fetchone()
    if is_exists:
        return jsonify({"message" : "해당 닉네임은 이미 존재합니다!"})
    c.execute("INSERT INTO users (nickname,password) VALUES (%s,%s)",(nickname,password))
    conn.commit()
    return jsonify({"message" : "회원가입이 완료되었습니다!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)