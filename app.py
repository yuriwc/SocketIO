from flask import Flask, json, request
from flask.templating import render_template
from flask_socketio import SocketIO, emit, join_room, send, leave_room

app = Flask(__name__)
io = SocketIO(app, cors_allowed_origins="*", async_handlers=True, pingTimeout=900)

@app.after_request
def after_request(resp):
    resp.headers.add('Access-Control-Allow-Origin', '*')
    resp.headers.add('Access-Control-Allow-Headers', 'Content-Type, X-Token')
    resp.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
    return resp

@app.route("/")
def home():
    return render_template("chat.html")

@io.on('join')
def on_join(data):
    print('--->entrou', data)
    username = data['username']
    room = data['room']
    join_room(room)
    #send(username + ' has entered the room.', to=room)
    emit("sentPrivateMessage", f"Welcome to {room}, {username}", room=room)

@io.on('leave')
def on_leave(data):
    print('leave', data)
    room = data['room']
    leave_room(room)

@io.on('sentMessage')
def sent_message_handle(msg):
    room = msg['room']
    message = msg['msg']
    emit('getMessage', message, broadcast=True, room=room)

@io.on('sentPrivateMessage')
def sent_message_handle(msg):
    print('entrandooooo')
    room = msg['room']
    message = msg['msg']
    emit('getMessagePrivate', message, broadcast=True, room=room)

if __name__ == "__main__":
    io.run(app, debug=True)