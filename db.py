import psycopg2, os
from psycopg2 import errors

# DBへの接続を開始する
def connect_db():
    username = os.getenv("USER")
    try:
        connection = psycopg2.connect(
            dbname="todo_app",
            user=username,
            host="localhost"
        )
    except errors.OperationalError:
        create_database()
        connection = psycopg2.connect(
            dbname="todo_app",
            user=username,
            host="localhost"
        )
    return connection

# データベースを作成する
def create_database():
    username = os.getenv("USER")
    con = psycopg2.connect(
        dbname="postgres",
        user=username,
        host="localhost"
    )
    con.autocommit = True
    try:
        cursor = con.cursor()
        cursor.execute("CREATE DATABASE todo_app")
        cursor.close()
    finally:
        con.close()

# todoテーブルを作成する
def init_db():
    con = connect_db()
    cursor = con.cursor()
    try:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS todo (
            todo_id SERIAL PRIMARY KEY,
            description VARCHAR(255) NOT NULL,
            completed BOOLEAN NOT NULL DEFAULT FALSE,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            deadline DATE
        );
        """)
        con.commit()
        cursor.close()
    finally:
        con.close()

# すべてのToDoの読み込み
def get_todos():
    con = connect_db()
    try:
        cur = con.cursor()
        cur.execute("SELECT * FROM todo;")
        todos = cur.fetchall()
        return todos
    finally:
        cur.close()
        con.close()

# ToDoの追加
def add_todo(description, deadline=None):
    con = connect_db()
    try:
        cur = con.cursor()
        cur.execute("""
            INSERT INTO todo (description, deadline)
            VALUES (%s, %s)
        """, (description, deadline))
        con.commit()
    finally:
        cur.close()
        con.close()

# ToDoの更新
def update_todo(todo_id):
    con = connect_db()
    try:
        cur = con.cursor()
        cur.execute("""
            UPDATE todo
            SET completed = TRUE,
                completed_at = CURRENT_TIMESTAMP,
                updated_at = CURRENT_TIMESTAMP
            WHERE todo_id = %s
        """, (todo_id,))
        con.commit()
    finally:
        cur.close()
        con.close()

# ToDoの編集
def edit_todo(todo_id, description, deadline=None):
    con = connect_db()
    try:
        cur = con.cursor()
        cur.execute("""
            UPDATE todo
            SET description = %s,
                deadline = %s,
                updated_at = CURRENT_TIMESTAMP
            WHERE todo_id = %s
            """, (description, deadline, todo_id))
        con.commit()
    finally:
        cur.close()
        con.close()

# ToDoの削除
def delete_todo(todo_id):
    con = connect_db()
    try:
        cur = con.cursor()
        cur.execute("DELETE FROM todo WHERE todo_id = %s", (todo_id,))
        con.commit()
    finally:
        cur.close()
        con.close()
