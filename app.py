from logging import debug
from flask import Flask, json
from flask.templating import render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
io = SocketIO(app, cors_allowed_origins="*", async_handlers=True, pingTimeout=900)

@app.route("/")
def home():
    return render_template("chat.html")

@io.on('sentMessage')
def sent_message_handle(msg):
    emit('getMessage', msg, broadcast=True)


if __name__ == "__main__":
    io.run(app)