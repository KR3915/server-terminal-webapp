from flask import Flask, render_template, request
import subprocess
import os
import logging
from datetime import datetime

app = Flask(__name__)

# Cesta k logu
log_path = "logs/log.txt"
ip_log_path = "logs/user_logs.txt"
# Vytvoření složky logs, pokud neexistuje
os.makedirs(os.path.dirname(log_path), exist_ok=True)
os.makedirs(os.path.dirname(ip_log_path), exist_ok=True)

#nastavení času
time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
# Nastavení logování

logging.basicConfig(
    filename=log_path,
    level=logging.INFO,
    format="[%(asctime)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

@app.route("/", methods=["GET", "POST"])
def index():
    user_ip = request.remote_addr
    logging.info(f"Request from {user_ip}")
    with open(ip_log_path, "a", encoding="utf-8") as f: #log ip
        f.write(f"\n[{time}] {user_ip}")
    
    if request.method == "POST":
        if "spustit_api" in request.form:
            return render_template("API.html")
        elif "spustit_b" in request.form:
            subprocess.Popen(["python3", "skript_b.py"])

    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
