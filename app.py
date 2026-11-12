import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

DB_PATH = "app.db"


def get_connection():
    """Открывает соединение с базой и настраивает доступ к полям по имени."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def fetch_all_tasks():
    """Возвращает все задачи. Используется и в GET, и в POST-ошибке."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, status FROM tasks ORDER BY id")
    rows = cursor.fetchall()
    conn.close()
    return rows


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        title = request.form.get("title", "").strip()

        if not title:
            return render_template(
                "index.html",
                items=fetch_all_tasks(),
                error="Название задачи не может быть пустым.",
            )

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
        conn.commit()
        conn.close()

        return redirect(url_for("index"))

    return render_template("index.html", items=fetch_all_tasks())


if __name__ == "__main__":
    app.run(debug=True, port=5000)
