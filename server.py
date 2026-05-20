from flask import Flask, request, jsonify
import sqlite3
import os

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

# ================= HOME =================
@app.route("/")
def home():
    return "BTC Clicker is running"

# ================= TELEGRAM AUTH =================
@app.route("/tg_auth", methods=["POST"])
def tg_auth():
    data = request.json

    user_id = str(data["id"])
    name = data.get("first_name", "player")

    cur.execute("SELECT * FROM users WHERE id=?", (user_id,))
    row = cur.fetchone()

    if not row:
        cur.execute(
            "INSERT INTO users VALUES (?, ?, ?, ?)",
            (user_id, name, 0, 1)
        )
        conn.commit()

    return jsonify({"ok": True, "id": user_id})

# ================= USER =================
@app.route("/user/<uid>")
def user(uid):
    cur.execute("SELECT * FROM users WHERE id=?", (uid,))
    row = cur.fetchone()

    if not row:
        cur.execute("INSERT INTO users VALUES (?, ?, ?, ?)", (uid, "unknown", 0, 1))
        conn.commit()
        row = (uid, "unknown", 0, 1)

    return jsonify({
        "id": row[0],
        "name": row[1],
        "coins": row[2],
        "power": row[3]
    })

# ================= SAVE =================
@app.route("/save", methods=["POST"])
def save():
    data = request.json

    cur.execute("""
        INSERT OR REPLACE INTO users VALUES (?, ?, ?, ?)
    """, (
        str(data["id"]),
        data["name"],
        int(data["coins"]),
        int(data["power"])
    ))

    conn.commit()
    return jsonify({"ok": True})

# ================= LEADERBOARD =================
@app.route("/leaderboard")
def leaderboard():
    cur.execute("""
        SELECT name, coins FROM users
        ORDER BY coins DESC
        LIMIT 10
    """)

    return jsonify([
        {"name": n, "coins": c}
        for n, c in cur.fetchall()
    ])

# ================= RUN =================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)