from flask_socketio import join_room, leave_room, emit
from flask_login import current_user
from extensions import socketio, db
from models import Message, ChatGroup, User
import datetime

users_online = set()

@socketio.on('join')
def on_join(data):
    room = data['room']
    join_room(room)
    users_online.add(current_user.username)
    emit('user_presence', list(users_online), room=room)

@socketio.on('leave')
def on_leave(data):
    room = data['room']
    leave_room(room)
    users_online.discard(current_user.username)
    emit('user_presence', list(users_online), room=room)

@socketio.on('typing')
def on_typing(data):
    emit('typing', { 'user': current_user.username }, room=data['room'])

@socketio.on('send_message')
def handle_message(data):
    room = data['room']
    content = data['content']
    msg = Message(content=content, sender=current_user, group_id=room)
    db.session.add(msg); db.session.commit()
    emit('new_message', {
        'user': current_user.username,
        'content': content,
        'timestamp': msg.timestamp.isoformat(),
        'message_id': msg.id
    }, room=room)

@socketio.on('message_read')
def handle_read(data):
    msg = Message.query.get(data['message_id'])
    user = User.query.get(current_user.id)
    msg.read_by.append(user)
    db.session.commit()
    emit('read_receipt', {
        'message_id': data['message_id'],
        'user': current_user.username
    }, room=data['room'])
