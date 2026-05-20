from flask import Flask, send_from_directory

app = Flask(__name__)

# главная страница
@app.route("/")
def home():
    return send_from_directory("static", "index.html")

# статика (css/js если будут)
@app.route("/<path:path>")
def static_files(path):
    return send_from_directory("static", path)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)