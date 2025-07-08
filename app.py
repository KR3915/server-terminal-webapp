from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "spustit_a" in request.form:
            subprocess.Popen(["python3", "skript_a.py"])
        elif "spustit_b" in request.form:
            subprocess.Popen(["python3", "skript_b.py"])
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
