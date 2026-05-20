from flask import Flask, request, jsonify, send_from_directory
import json
import os

app = Flask(__name__)

FILE = "users.json"

# ===== LOAD DATA =====
def load():
    if os.path.exists(FILE):
        return json.load(open(FILE, "r"))
    return {}

def save(data):
    json.dump(data, open(FILE, "w"))

users = load()

# ===== WEB =====
@app.route("/")
def home():
    return send_from_directory("static", "index.html")

# ===== SAVE PLAYER =====
@app.route("/api/save", methods=["POST"])
def save_player():
    global users

    data = request.json
    uid = str(data["id"])

    users[uid] = {
        "name": data.get("name"),
        "coins": data.get("coins", 0),
        "level": data.get("level", 1),
        "power": data.get("power", 1)
    }

    save(users)
    return {"ok": True}

# ===== GET USER =====
@app.route("/api/user/<uid>")
def get_user(uid):
    return jsonify(users.get(uid, {}))

# ===== LEADERBOARD =====
@app.route("/api/top")
def top():
    sorted_users = sorted(users.items(), key=lambda x: x[1]["coins"], reverse=True)

    return jsonify([
        {
            "id": uid,
            "name": u["name"],
            "coins": u["coins"],
            "level": u["level"]
        }
        for uid, u in sorted_users[:10]
    ])

# ===== RUN =====
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)