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
            deadline DATE,
            priority INTEGER DEFAULT 3,
            notes TEXT,
            progress INTEGER DEFAULT 0 CHECK (progress >= 0 AND progress <= 100)
        );
        """)
        con.commit()
        cursor.close()
    finally:
        con.close()

# すべてのToDoの読み込み（期限日でソート）
def get_todos():
    con = connect_db()
    try:
        cur = con.cursor()
        # 未完了のToDoは期限日の昇順（NULLは最後）
        # 完了済みのToDoは完了日時の降順
        cur.execute("""
            (
                SELECT * FROM todo
                WHERE completed = FALSE
                ORDER BY
                    CASE
                        WHEN deadline IS NULL THEN 1
                        ELSE 0
                    END,
                    deadline ASC,
                    created_at ASC
            )
            UNION ALL
            (
                SELECT * FROM todo
                WHERE completed = TRUE
                ORDER BY completed_at DESC
            );
        """)
        todos = cur.fetchall()
        return todos
    finally:
        cur.close()
        con.close()

# ToDoの追加
def add_todo(description, deadline=None, priority=2, notes=''):
    con = connect_db()
    try:
        cur = con.cursor()
        cur.execute("""
            INSERT INTO todo (description, deadline, priority, notes)
            VALUES (%s, %s, %s, %s)
        """, (description, deadline, priority, notes))
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
def edit_todo(todo_id, description, deadline=None, priority=None, notes=None, progress=None):
    con = connect_db()
    try:
        cur = con.cursor()

        # 現在の値を取得
        cur.execute("""
            SELECT priority, notes, progress
            FROM todo
            WHERE todo_id = %s
        """, (todo_id))
        current_values = cur.fetchone()

        # 入力がない場合は現在の値を使用する
        if priority is None and current_values:
            priority = current_values[0]
        if notes is None and current_values:
            notes = current_values[1]
        if progress is None and current_values:
            progress = current_values[2]

        # 更新クエリ実行
        cur.execute("""
            UPDATE todo
            SET description = %s,
                deadline = %s,
                priority = %s,
                notes = %s,
                progress = %s,
                updated_at = CURRENT_TIMESTAMP
            WHERE todo_id = %s
            """, (description, deadline, priority, notes, progress, todo_id))
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

# ToDoの編集内容を保存
def save_todo(todo_id, description, deadline, priority, progress, notes):
    con = connect_db()
    try:
        cur = con.cursor()
        cur.execute("""
            UPDATE todo
            SET description = %s,
                deadline = %s,
                priority = %s,
                progress = %s,
                notes = %s,
                updated_at = CURRENT_TIMESTAMP
            WHERE todo_id = %s
        """, (description, deadline, priority, progress, notes, todo_id))
        con.commit()
    finally:
        cur.close()
        con.close()

# ToDoを未完了に戻す
def revert_todo(todo_id):
    con = connect_db()
    try:
        cur = con.cursor()
        cur.execute("""
            UPDATE todo
            SET completed = FALSE,
                completed_at = CURRENT_TIMESTAMP,
                updated_at = CURRENT_TIMESTAMP
            WHERE todo_id = %s
        """, (todo_id,))
        con.commit()
    finally:
        cur.close()
        con.close()
