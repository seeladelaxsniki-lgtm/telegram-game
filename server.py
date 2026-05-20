from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# ================= DB =================
conn = sqlite3.connect("game.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    name TEXT,
    coins INTEGER,
    power INTEGER
)
""")
conn.commit()

# ================= SAVE USER =================
@app.route("/save", methods=["POST"])
def save():
    data = request.json

    user_id = str(data["id"])
    name = data["name"]
    coins = int(data["coins"])
    power = int(data["power"])

    cur.execute("""
    INSERT OR REPLACE INTO users VALUES (?, ?, ?, ?)
    """, (user_id, name, coins, power))

    conn.commit()

    return jsonify({"ok": True})

# ================= GET USER =================
@app.route("/user/<uid>")
def user(uid):
    cur.execute("SELECT * FROM users WHERE id=?", (uid,))
    row = cur.fetchone()

    if not row:
        return jsonify({
            "id": uid,
            "name": "unknown",
            "coins": 0,
            "power": 1
        })

    return jsonify({
        "id": row[0],
        "name": row[1],
        "coins": row[2],
        "power": row[3]
    })

# ================= LEADERBOARD =================
@app.route("/leaderboard")
def leaderboard():
    cur.execute("""
        SELECT name, coins
        FROM users
        ORDER BY coins DESC
        LIMIT 10
    """)

    data = cur.fetchall()

    return jsonify([
        {"name": x[0], "coins": x[1]}
        for x in data
    ])

# ================= RUN =================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)