from flask import Blueprint, request, jsonify
from models import db, TodoList
from datetime import datetime
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

@todo_bp.route('/todo/result', methods = ['GET'])
def get_task_by_emotion() :
    emotion = request.args.get('emotion')
    if not emotion :
        return jsonify({'error' : 'emotion parameter is required'}), 400
    todos = TodoList.query.filter_by(emotion = emotion).all()
    if not todos :
        return jsonify({'message' : f'No todos fount for emotion"{emotion}"'}),404
    try :
        todos = sorted(
            todos,
            key = lambda t: datetime.strptime(t.deadline, '%Y-%m-%d') if isinstance(t.deadline, str) else t.deadline
        )
    except Exception as e :
        return jsonify({'error' : f'Deadline format error : {str(e)}'}), 500
    
    nearest_todo = todos[0]

    return jsonify({
        'id' : nearest_todo.id,
        'title' : nearest_todo.title,
        'deadline' : nearest_todo.deadline,
        'emotion' : nearest_todo.emotion
    })



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
