from flask import Blueprint, request, jsonify
from models import db, TodoList

todo_bp = Blueprint('todo', __name__)


@todo_bp.route('/todo', methods = ['POST'])
def add_todo():
    data = request.get_json()
    new_todo = TodoList(title = data['title'], deadline = data['deadline'], emotion = data['emotion'])
    db.session.add(new_todo)
    db.session.commit()
    return jsonify({'message' : 'Todo created'})

@todo_bp.route('/todos', methods = ['GET'])
def get_todos():
    todos = TodoList.query.all()
    return jsonify([{'id' : t.id, 
                    'title' : t.title, 
                    'deadline' : t.deadline, 
                    'emotion' : t.emotion} for t in todos])

@todo_bp.route('/todos/<int:todo_id>', methods = ['PUT'])
def update_todo(todo_id):
    todo = TodoList.query.get_or_404(todo_id)
    data = request.get_json()
    todo.title = data.get('title', TodoList.title)
    todo.deadline = data.get('deadline', TodoList.deadline)
    todo.emotion = data.get('emotion', TodoList.emotion)
    db.session.commit()
    return jsonify({'message':'Todo updated'})

@todo_bp.route('/todos/<int:todo_id>', methods = ['delete'])
def delete_todo(todo_id) :
    todo = TodoList.query.get_or_404(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return jsonify({'message' : 'Todo deleted'})
