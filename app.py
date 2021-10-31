from logging import debug
from flask import Flask, json
from flask.templating import render_template
from flask_socketio import SocketIO, emit

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

@io.on('sentMessage')
def sent_message_handle(msg):
    emit('getMessage', msg, broadcast=True)


if __name__ == "__main__":
    io.run(app)