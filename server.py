from flask import Flask, send_from_directory

app = Flask(__name__)

# 🏠 ГЛАВНАЯ СТРАНИЦА
@app.route("/")
def home():
    return send_from_directory("static", "index.html")


# (опционально) если есть файлы типа js/css
@app.route("/<path:path>")
def static_files(path):
    return send_from_directory("static", path)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)