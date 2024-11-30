from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_login import LoginManager, login_user, current_user, UserMixin, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'secret_key'

socketio = SocketIO(app, cors_allowed_origins='*')

login_manager = LoginManager()
login_manager.init_app(app)

users = {
    'user1': {'password': generate_password_hash('password123')}, 
    'user2': {'password': generate_password_hash('password456')}
}

class User(UserMixin):
    def __init__(self, username):
        self.id = username

@login_manager.user_loader
def load_user(username):
    if username in users:
        return User(username)
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login/<username>', methods=['GET'])
def login(username):
    if username in users:
        user = User(username)
        login_user(user)
        return jsonify({"message": "Logged in successfully!", "username": username})
    return jsonify({"message": "Invalid credentials"}), 401

@socketio.on('connect')
def handle_connect():
    if current_user.is_authenticated:
        emit('status', {'msg': f'{current_user.id} connected.'})
    else:
        emit('status', {'msg': 'Please log in to start chatting.'})

@socketio.on('message')
def handle_message(data):
    if current_user.is_authenticated:
        msg = data['msg']
        sender = data['sender']
        room = data['room']
        emit('message', {'msg': msg, 'sender': sender}, room=room)
    else:
        emit('status', {'msg': 'You must be logged in to send messages.'})

@socketio.on('join')
def handle_join(room):
    if current_user.is_authenticated:
        join_room(room)
        emit('status', {'msg': f'{current_user.id} has joined room {room}'}, room=room)
    else:
        emit('status', {'msg': 'You must be logged in to join a room.'})

@socketio.on('leave')
def handle_leave(room):
    if current_user.is_authenticated:
        leave_room(room)
        emit('status', {'msg': f'{current_user.id} has left room {room}'}, room=room)
    else:
        emit('status', {'msg': 'You must be logged in to leave a room.'})

@socketio.on('disconnect')
def handle_disconnect():
    emit('status', {'msg': 'A user disconnected.'})

if __name__ == '__main__':
    socketio.run(app, debug=True)
