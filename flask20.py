from flask import Flask, request,redirect,render_template,session,url_for
import pymysql
from DB_password import DBpassword
app = Flask(__name__)
app.secret_key = "땅크"
def mk_db():
    conn = pymysql.connect(
        host="localhost",
        user="root",
        passwd=DBpassword.pw()
    )
    c = conn.cursor()
    c.execute("CREATE DATABASE IF NOT EXISTS flask20")
    conn.commit()
    conn.close()
def connector():
    return pymysql.connect(
        host = "localhost",
        user="root",
        passwd="Zdzdsmsm44!",
        database="flask20"
    )
def init_db():
    conn = connector()
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS posts(
              id INT AUTO_INCREMENT PRIMARY KEY,
              nickname TEXT,
              title TEXT,
              content TEXT
              )
              """)
    c.execute("""CREATE TABLE IF NOT EXISTS users(
              nickname VARCHAR(30),
              password TEXT 
              )
              """)
    c.execute("""CREATE TABLE IF NOT EXISTS likes(
              like_count INT AUTO_INCREMENT PRIMARY KEY,
              nickname TEXT,
              post_id INT
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
    conn.commit()
    conn.close()
    return render_template("20index.html",posts=posts,nickname=nickname)

@app.route('/register',methods=["GET","POST"])
def register():
    if request.method == "GET":
        return render_template("20register.html")
    conn = connector()
    c = conn.cursor()
    nickname = request.form["nickname"]
    password = request.form["password"]
    c.execute("SELECT * FROM users WHERE nickname = %s",(nickname,))
    is_exists = c.fetchone()
    if is_exists:
        return render_template("20register.html", error="이미 존재하는 닉네임")
    c.execute("INSERT INTO users (nickname,password) VALUES (%s,%s)",(nickname,password))
    conn.commit()
    conn.close()
    session["user"] = nickname
    return redirect(url_for("home"))

@app.route('/login',methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("20login.html")
    conn = connector()
    c = conn.cursor()
    nickname = request.form["nickname"]
    password = request.form["password"]
    c.execute("SELECT * FROM users WHERE nickname = %s AND password = %s",(nickname,password))
    is_login = c.fetchone()
    if not is_login:
        return render_template("20login.html",fail_login="닉네임과 비밀번호를 다시 확인하십시오!")
    session["user"] = nickname
    conn.close()
    return redirect(url_for('home'))

@app.route('/write',methods=["GET","POST"])
def write():
    nickname = session.get("user")
    if not nickname:
        return redirect(url_for('login'))
    if request.method == "GET":
        return render_template("20write.html")
    title = request.form["title"]
    content = request.form["content"]
    conn = connector()
    c = conn.cursor()
    c.execute("INSERT INTO posts (nickname,title,content) VALUES (%s,%s,%s)",(nickname,title,content))
    conn.commit()
    conn.close()
    return redirect(url_for('home'))

@app.route('/post/<int:post_id>')
def detail(post_id):
    conn = connector()
    c = conn.cursor()
    c.execute("SELECT * FROM posts WHERE id = %s",(post_id,))
    posts = c.fetchone()
    c.execute("SELECT * FROM likes WHERE post_id = %s ",(post_id,))
    likes = c.fetchall()
    c.execute("SELECT * FROM comments WHERE post_id = %s ",(post_id,))
    comments = c.fetchall()
    conn.close()
    return render_template("20detail.html",posts=posts,likes=likes,comments=comments)


@app.route('/post/<int:post_id>/delete',methods=["POST"])
def detail_delete(post_id):
    nickname = session.get("user")
    if not nickname:
        return redirect(url_for('login'))
    conn = connector()
    c = conn.cursor()
    c.execute("SELECT * FROM posts WHERE nickname = %s",(nickname,))
    is_delete = c.fetchone()
    if not is_delete:
        return "자신의 글만 삭제 할 수 있습니다"
    c.execute("DELETE FROM posts WHERE id = %s",(post_id))
    conn.commit()
    conn.close()
    return redirect(url_for('home'))

@app.route('/post/<int:post_id>/like',methods=["POST"])
def detail_like(post_id):
    nickname = session.get("user")
    if not nickname:
        return redirect(url_for('login'))
    conn = connector()
    c = conn.cursor()
    c.execute("SELECT * FROM likes WHERE nickname = %s AND post_id = %s",(nickname,post_id))
    is_exists = c.fetchone()
    if is_exists:
        return "이미 좋아요를 눌렀습니다!"
    c.execute("INSERT INTO likes (nickname,post_id) VALUES (%s,%s)",(nickname,post_id))
    conn.commit()
    conn.close()
    return redirect(url_for('detail', post_id=post_id))

    
@app.route('/post/<int:post_id>/comment',methods=["POST"])
def detail_comment(post_id):
    nickname = session.get("user")
    if not nickname:
        return redirect(url_for('login'))
    content = request.form["content"]
    conn = connector()
    c = conn.cursor()
    c.execute("INSERT INTO comments (nickname,content,post_id) VALUES (%s,%s,%s)",(nickname,content,post_id))
    conn.commit()
    conn.close()
    return redirect(url_for('detail', post_id=post_id))
mk_db()
init_db()
if __name__ == "__main__":
    app.run(host="localhost",port=5050,debug=True)