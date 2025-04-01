from flask import Flask, request, render_template
from datetime import datetime
import db

app = Flask(__name__)
db.init_db()

# ToDoの表示
@app.route('/')
def show_todos():
    todos = db.get_todos()
    return render_template('index.html', todos=todos)

# 新規ToDoの作成
@app.route('/create_todo', methods=['POST'])
def create_todo():
    description = request.form['description']
    deadline = request.form.get('deadline')
    priority = request.form.get('priority', 3)
    notes = request.form.get('notes')
    progress = request.form.get('progress', 0)

    if deadline:
        deadline = datetime.strptime(deadline, '%Y-%m-%d').date()
        
    try:
        priority = int(priority)
    except (ValueError, TypeError):
        priority = 3
        
    try:
        progress = int(progress)
        if progress < 0:
            progress = 0
        elif progress > 100:
            progress = 100
    except (ValueError, TypeError):
        progress = 0

    db.add_todo(description, deadline, priority, notes, progress)
    return show_todos()

# ToDoの完了
@app.route('/update_todo', methods=['POST'])
def update_todo():
    todo_id = request.form['todo_id']
    db.update_todo(todo_id)
    return show_todos()

# ToDoの編集保存
@app.route('/save_todo', methods=['POST'])
def save_todo():  
    # フォームデータの取得
    todo_id = request.form['todo_id']
    new_description = request.form['new_description']
    new_deadline = request.form.get('new_deadline')
    new_priority = request.form.get('new_priority')
    new_notes = request.form.get('new_notes')
    new_progress = request.form.get('new_progress')
    
    if new_deadline:
        new_deadline = datetime.strptime(new_deadline, '%Y-%m-%d').date()
        
    try:
        new_priority = int(new_priority) if new_priority else None
    except (ValueError, TypeError):
        new_priority = None
        
    try:
        new_progress = int(new_progress) if new_progress else None
        if new_progress is not None:
            if new_progress < 0:
                new_progress = 0
            elif new_progress > 100:
                new_progress = 100
    except (ValueError, TypeError):
        new_progress = None
        
    db.edit_todo(todo_id, new_description, new_deadline, new_priority, new_notes, new_progress)
    return show_todos()

# ToDoの削除
@app.route('/delete_todo', methods=['POST'])
def delete_todo():
    todo_id = request.form['todo_id']
    db.delete_todo(todo_id)
    return show_todos()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)