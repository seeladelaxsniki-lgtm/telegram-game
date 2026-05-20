from flask import Flask, request, jsonify, send_from_directory
import os

app = Flask(__name__)

# ===== SIMPLE DB IN MEMORY =====
users = {}

# ===== FRONTEND =====
@app.route("/")
def home():
    return send_from_directory("static", "index.html")

# ===== SAVE PLAYER =====
@app.route("/api/save", methods=["POST"])
def save():
    data = request.json
    uid = str(data.get("id"))

    users[uid] = {
        "name": data.get("name", "player"),
        "coins": data.get("coins", 0),
        "level": data.get("level", 1),
        "power": data.get("power", 1)
    }

    return jsonify({"ok": True})

# ===== GET PLAYER =====
@app.route("/api/user/<uid>")
def get_user(uid):
    return jsonify(users.get(uid, {
        "name": "unknown",
        "coins": 0,
        "level": 1,
        "power": 1
    }))

# ===== LEADERBOARD =====
@app.route("/api/top")
def top():
    sorted_users = sorted(
        users.items(),
        key=lambda x: x[1]["coins"],
        reverse=True
    )

    result = [
        {
            "id": uid,
            "name": data["name"],
            "coins": data["coins"],
            "level": data["level"]
        }
        for uid, data in sorted_users[:10]
    ]

    return jsonify(result)

# ===== RUN =====
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)