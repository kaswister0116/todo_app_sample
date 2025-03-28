from flask import Flask, request, render_template
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
    db.add_todo(description)
    return show_todos()

# ToDoの完了
@app.route('/update_todo', methods=['POST'])
def update_todo():
    todo_id = request.form['todo_id']
    db.update_todo(todo_id)
    return show_todos()

# ToDoの削除
@app.route('/delete_todo', methods=['POST'])
def delete_todo():
    todo_id = request.form['todo_id']
    db.delete_todo(todo_id)
    return show_todos()

if __name__ == '__main__':
     app.run(host='127.0.0.1', port=8080, debug=True)
