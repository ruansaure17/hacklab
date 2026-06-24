import os
import sqlite3
import hashlib
from flask import Flask, request, render_template, redirect, session, url_for, g, send_from_directory

APP_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(APP_DIR, "lab.db")
UPLOAD_DIR = os.path.join(APP_DIR, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = Flask(__name__)
app.secret_key = "supersecretkey123"


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(exc):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    fresh = not os.path.exists(DB_PATH)
    db = sqlite3.connect(DB_PATH)
    cur = db.cursor()
    cur.executescript(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT DEFAULT 'user',
            bio TEXT DEFAULT '',
            secret_note TEXT DEFAULT ''
        );

        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id INTEGER,
            author TEXT,
            content TEXT
        );

        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            body TEXT
        );
        """
    )
    if fresh:
        def h(p):
            return hashlib.md5(p.encode()).hexdigest()

        cur.execute(
            "INSERT INTO users (username, password, role, bio, secret_note) VALUES (?, ?, ?, ?, ?)",
            ("admin", h("admin123"), "admin", "Administrador do sistema.", "FLAG{painel_admin_alcancado}"),
        )
        cur.execute(
            "INSERT INTO users (username, password, role, bio, secret_note) VALUES (?, ?, ?, ?, ?)",
            ("alice", h("alice123"), "user", "Oi, sou a Alice!", "nota pessoal da alice"),
        )
        cur.execute(
            "INSERT INTO users (username, password, role, bio, secret_note) VALUES (?, ?, ?, ?, ?)",
            ("bob", h("bob123"), "user", "Bob, dev júnior.", "nota pessoal do bob"),
        )
        cur.execute(
            "INSERT INTO posts (title, body) VALUES (?, ?)",
            ("Bem-vindo ao Lab", "Este é um laboratório de testes de segurança web. Explore à vontade."),
        )
        cur.execute(
            "INSERT INTO posts (title, body) VALUES (?, ?)",
            ("Atualização do sistema", "Corrigimos alguns bugs de performance nesta semana."),
        )
        db.commit()
    db.close()


@app.route("/")
def index():
    db = get_db()
    posts = db.execute("SELECT * FROM posts").fetchall()
    return render_template("index.html", posts=posts, user=session.get("username"))


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        pwd_hash = hashlib.md5(password.encode()).hexdigest()
        db = get_db()
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{pwd_hash}'"
        cur = db.execute(query)
        user = cur.fetchone()
        if user:
            session["username"] = user["username"]
            session["role"] = user["role"]
            session["user_id"] = user["id"]
            return redirect(url_for("index"))
        else:
            error = "Usuário ou senha inválidos."
    return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


@app.route("/register", methods=["GET", "POST"])
def register():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        db = get_db()
        try:
            db.execute(
                "INSERT INTO users (username, password, role, bio) VALUES (?, ?, ?, ?)",
                (username, hashlib.md5(password.encode()).hexdigest(), "user", ""),
            )
            db.commit()
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            error = "Usuário já existe."
    return render_template("register.html", error=error)


@app.route("/search")
def search():
    q = request.args.get("q", "")
    db = get_db()
    results = []
    if q:
        cur = db.execute(f"SELECT id, title, body FROM posts WHERE title LIKE '%{q}%'")
        results = cur.fetchall()
    return render_template("search.html", query=q, results=results)


@app.route("/profile/<username>")
def profile(username):
    db = get_db()
    user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    if not user:
        return "Usuário não encontrado", 404
    return render_template("profile.html", profile=user, viewer=session.get("username"))


@app.route("/profile/<username>/edit", methods=["GET", "POST"])
def edit_profile(username):
    db = get_db()
    user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    if not user:
        return "Usuário não encontrado", 404
    if request.method == "POST":
        new_bio = request.form.get("bio", "")
        db.execute("UPDATE users SET bio = ? WHERE username = ?", (new_bio, username))
        db.commit()
        return redirect(url_for("profile", username=username))
    return render_template("edit_profile.html", profile=user)


@app.route("/admin")
def admin():
    if session.get("role") != "admin":
        return render_template("admin.html", authorized=False, users=None)
    db = get_db()
    users = db.execute("SELECT * FROM users").fetchall()
    return render_template("admin.html", authorized=True, users=users)


@app.route("/admin/delete/<int:user_id>")
def admin_delete(user_id):
    db = get_db()
    db.execute("DELETE FROM users WHERE id = ?", (user_id,))
    db.commit()
    return redirect(url_for("admin"))


@app.route("/post/<int:post_id>", methods=["GET", "POST"])
def post_detail(post_id):
    db = get_db()
    post = db.execute("SELECT * FROM posts WHERE id = ?", (post_id,)).fetchone()
    if not post:
        return "Post não encontrado", 404
    if request.method == "POST":
        author = request.form.get("author", "anônimo")
        content = request.form.get("content", "")
        db.execute(
            "INSERT INTO comments (post_id, author, content) VALUES (?, ?, ?)",
            (post_id, author, content),
        )
        db.commit()
    comments = db.execute("SELECT * FROM comments WHERE post_id = ?", (post_id,)).fetchall()
    return render_template("post.html", post=post, comments=comments)


@app.route("/upload", methods=["GET", "POST"])
def upload():
    message = None
    if request.method == "POST":
        f = request.files.get("file")
        if f and f.filename:
            save_path = os.path.join(UPLOAD_DIR, f.filename)
            f.save(save_path)
            message = f"Arquivo enviado: {f.filename}"
    files = os.listdir(UPLOAD_DIR)
    return render_template("upload.html", message=message, files=files)


@app.route("/uploads/<path:filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_DIR, filename)


@app.route("/file")
def file_view():
    name = request.args.get("name", "info.txt")
    path = os.path.join(APP_DIR, "files", name)
    try:
        with open(path, "r", errors="ignore") as fh:
            content = fh.read()
    except Exception as e:
        content = f"Erro ao ler arquivo: {e}"
    return render_template("file.html", name=name, content=content)


@app.route("/api/user/<int:user_id>")
def api_user(user_id):
    db = get_db()
    user = db.execute("SELECT id, username, role, bio, secret_note FROM users WHERE id = ?", (user_id,)).fetchone()
    if not user:
        return {"error": "not found"}, 404
    return {
        "id": user["id"],
        "username": user["username"],
        "role": user["role"],
        "bio": user["bio"],
        "secret_note": user["secret_note"],
    }


if __name__ == "__main__":
    init_db()
    os.makedirs(os.path.join(APP_DIR, "files"), exist_ok=True)
    info_file = os.path.join(APP_DIR, "files", "info.txt")
    if not os.path.exists(info_file):
        with open(info_file, "w") as fh:
            fh.write("Este é um arquivo de informações públicas do laboratório.\n")
    app.run(host="0.0.0.0", port=5000, debug=True)
