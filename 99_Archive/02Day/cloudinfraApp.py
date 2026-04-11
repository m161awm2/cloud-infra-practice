from flask import Flask,request,redirect,render_template,session,url_for
import pymysql
from config import Config
config = Config()
app = Flask(__name__)
app.secret_key = config.db_pw()

def make_db():
    conn = pymysql.connect(
        host=config.edp(),
        user="admin",
        passwd=config.db_pw(),
    )
    c = conn.cursor()
    c.execute("CREATE DATABASE IF NOT EXISTS day02")
    conn.commit()
    conn.close()

def connector():
    return pymysql.connect(
        host=config.edp(),
        user="admin",
        passwd=config.db_pw(),
        database="day02"
    )

def init_db():
    conn = connector()
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS posts(
              id INT AUTO_INCREMENT PRIMARY KEY,
              nickname TEXT,
              title VARCHAR(20),
              content TEXT
              )
              """)
    c.execute("""CREATE TABLE IF NOT EXISTS users(
              nickname VARCHAR(14),
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
    nickname = session.get("user")
    conn = connector()
    c = conn.cursor()
    c.execute("SELECT * FROM posts ORDER BY id DESC")
    posts = c.fetchall()
    conn.close()
    return render_template("index.html",posts=posts,nickname=nickname)

@app.route('/register',methods=["GET","POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    nickname = request.form["nickname"]
    password = request.form["password"]
    conn = connector()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE nickname = %s",(nickname,))
    is_exists = c.fetchone()
    if is_exists:
        return "중복"
    c.execute("INSERT INTO users (nickname, password) VALUES (%s,%s)",(nickname,password))
    conn.commit()
    conn.close()
    return redirect(url_for('home'))

@app.route('/login',methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    conn = connector()
    c = conn.cursor()
    nickname = request.form["nickname"]
    password = request.form["password"]
    c.execute("SELECT * FROM users WHERE nickname = %s AND password = %s",(nickname,password))
    is_login = c.fetchone()
    if not is_login:
        return "닉네임과 비밀번호를 다시 확인하세요!"
    session["user"] = nickname
    return redirect(url_for('home'))

@app.route('/write',methods=["GET","POST"])
def write():
    if request.method == "GET":
        return render_template("write.html")
    nickname = session.get("user")
    if not nickname:
        return "로그인 후 사용 가능한 기능입니다."
    conn = connector()
    c = conn.cursor()
    title = request.form["title"]
    content = request.form["content"]
    c.execute("INSERT INTO posts (nickname,title,content) VALUES (%s,%s,%s)",(nickname,title,content))
    conn.commit()
    conn.close()
    return redirect(url_for("home"))

@app.route('/post/<int:post_id>')
def detail(post_id):
    conn = connector()
    c = conn.cursor()
    c.execute("SELECT * FROM posts WHERE id = %s",(post_id,))
    post = c.fetchone()
    c.execute("SELECT * FROM comments WHERE post_id = %s",(post_id,))
    comment = c.fetchall()
    conn.close()
    return render_template("detail.html",post=post,comment=comment)

@app.route('/post/<int:post_id>/comment',methods=["POST"])
def comment(post_id):
    nickname = session.get("user")
    if not nickname:
        return "해당 기능은 로그인후 쓰세요"
    content = request.form["content"]
    conn = connector()
    c = conn.cursor()
    c.execute("INSERT INTO comments (nickname,content,post_id) VALUES (%s,%s,%s)",(nickname,content,post_id))
    conn.commit()
    conn.close()
    return redirect(url_for('detail', post_id=post_id))

make_db()
init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=80,debug=True)