from flask import Flask, render_template, request
import subprocess
import os
import logging
from datetime import datetime
from flask_socketio import SocketIO
from ptyprocess import PtyProcessUnicode

app = Flask(__name__)
socketio = SocketIO(app, async_mode="threading", logger=True, engineio_logger=True)

pty_proc = None

# Logování
log_path = "logs/log.txt"
ip_log_path = "logs/user_logs.txt"
os.makedirs(os.path.dirname(log_path), exist_ok=True)
os.makedirs(os.path.dirname(ip_log_path), exist_ok=True)

logging.basicConfig(
    filename=log_path,
    level=logging.INFO,
    format="[%(asctime)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

@app.route("/", methods=["GET", "POST"])
def index():
    user_ip = request.remote_addr
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logging.info(f"Request from {user_ip}")
    with open(ip_log_path, "a", encoding="utf-8") as f:
        f.write(f"\n[{time}] {user_ip}")
    
    if request.method == "POST":
        if "spustit_api" in request.form:
            return render_template("API.html")
        elif "spustit_b" in request.form:
            subprocess.Popen(["python3", "skript_b.py"])

    return render_template("index.html")

@socketio.on('connect')
def on_connect():
    global pty_proc
    if pty_proc is None:
        pty_proc = PtyProcessUnicode.spawn(['bash'])
        socketio.start_background_task(read_output)

def read_output():
    while True:
        try:
            if pty_proc is not None:
                output = pty_proc.read(1024)
                if output:
                    print(f"[DEBUG] OUTPUT: {output}")
                    socketio.emit('output', output)
        except Exception as e:
            socketio.sleep(0.1)


@socketio.on('input')
def on_input(data):
    if pty_proc:
        pty_proc.write(data)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
