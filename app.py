from flask import Flask, request, render_template, redirect, url_for
from datetime import datetime, date
import db

app = Flask(__name__)
db.init_db()

# ToDoの表示
@app.route('/')
def show_todos():
    todos = db.get_todos()
    return render_template('index.html', todos=todos, current_date=date.today())

# 新規ToDoの作成
@app.route('/create_todo', methods=['POST'])
def create_todo():
    description = request.form.get('description')
    deadline = request.form.get('deadline')
    priority = request.form.get('priority', '中')  # デフォルト値中
    notes = request.form.get('notes', '')  # デフォルト値空文字

    # 優先度を数値に変換
    priority_map = {'高': 1, '中': 2, '低': 3}
    try:
        priority = priority_map.get(priority, 2)  # デフォルト値2
    except ValueError:
        priority = 2

    # 期限日が指定されている場合のみ設定
    if deadline:
        db.add_todo(description, deadline, priority, notes)
    else:
        db.add_todo(description, priority=priority, notes=notes)

    return redirect(url_for('show_todos'))

# ToDoの完了
@app.route('/update_todo', methods=['POST'])
def update_todo():
    todo_id = request.form['todo_id']
    db.update_todo(todo_id)
    return redirect(url_for('show_todos'))

# ToDoの削除
@app.route('/delete_todo', methods=['POST'])
def delete_todo():
    todo_id = request.form['todo_id']
    db.delete_todo(todo_id)
    return redirect(url_for('show_todos'))

# ToDoの編集内容を保存
@app.route('/save_todo', methods=['POST'])
def save_todo():
    todo_id = request.form['todo_id']
    description = request.form['new_description']
    deadline = request.form.get('new_deadline')
    priority = request.form.get('priority', '中')  # デフォルト値中
    progress = request.form.get('new_progress', '0')
    notes = request.form.get('new_notes', '')

    if deadline:
        deadline = datetime.strptime(deadline, '%Y-%m-%d').date()

    # 進捗を整数に変換
    try:
        progress = int(progress)
        if progress < 0:
            progress = 0
        elif progress > 100:
            progress = 100
    except ValueError:
        progress = 0

    # 優先度を数値に変換
    priority_map = {'高': 1, '中': 2, '低': 3}
    try:
        priority = priority_map.get(priority, 2)  # デフォルト値2
    except ValueError:
        priority = 2

    db.save_todo(todo_id, description, deadline, priority, progress, notes)
    return redirect(url_for('show_todos'))

# ToDoを未完了に戻す
@app.route('/revert_todo', methods=['POST'])
def revert_todo():
    todo_id = request.form['todo_id']
    db.revert_todo(todo_id)
    return redirect(url_for('show_todos'))

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
