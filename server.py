from flask import Flask, request, jsonify, send_from_directory
import sqlite3
import os

app = Flask(__name__)

conn = sqlite3.connect("game.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    name TEXT,
    coins INTEGER,
    power INTEGER,
    energy INTEGER
)
""")
conn.commit()

MAX_ENERGY = 100

@app.route("/")
def home():
    return send_from_directory(".", "index.html")

@app.route("/tg_auth", methods=["POST"])
def tg_auth():
    data = request.json
    uid = str(data["id"])
    name = data.get("first_name", "player")

    cur.execute("SELECT * FROM users WHERE id=?", (uid,))
    row = cur.fetchone()

    if not row:
        cur.execute(
            "INSERT INTO users VALUES (?, ?, ?, ?, ?)",
            (uid, name, 0, 1, MAX_ENERGY)
        )
        conn.commit()

    return jsonify({"ok": True, "id": uid})

@app.route("/user/<uid>")
def user(uid):
    cur.execute("SELECT * FROM users WHERE id=?", (uid,))
    row = cur.fetchone()

    if not row:
        return jsonify({
            "id": uid,
            "name": "unknown",
            "coins": 0,
            "power": 1,
            "energy": MAX_ENERGY
        })

    return jsonify({
        "id": row[0],
        "name": row[1],
        "coins": row[2],
        "power": row[3],
        "energy": row[4]
    })

@app.route("/tap", methods=["POST"])
def tap():
    data = request.json
    uid = str(data["id"])

    cur.execute("SELECT coins, power, energy FROM users WHERE id=?", (uid,))
    row = cur.fetchone()

    if not row:
        return jsonify({"error": "no user"})

    coins, power, energy = row

    if energy <= 0:
        return jsonify({"ok": False, "reason": "no energy"})

    import random
    crit = 2 if random.random() < 0.1 else 1

    coins += power * crit
    energy -= 1

    cur.execute("""
        UPDATE users
        SET coins=?, energy=?
        WHERE id=?
    """, (coins, energy, uid))

    conn.commit()

    return jsonify({
        "coins": coins,
        "energy": energy,
        "crit": crit
    })

@app.route("/buy", methods=["POST"])
def buy():
    data = request.json
    uid = str(data["id"])
    item = data["item"]

    cur.execute("SELECT coins, power, energy FROM users WHERE id=?", (uid,))
    coins, power, energy = cur.fetchone()

    if item == "p1":
        cost = 150
        if coins >= cost:
            coins -= cost
            power += 1

    if item == "p2":
        cost = 400
        if coins >= cost:
            coins -= cost
            power += 2

    cur.execute("""
        UPDATE users SET coins=?, power=?, energy=? WHERE id=?
    """, (coins, power, energy, uid))

    conn.commit()

    return jsonify({"coins": coins, "power": power})

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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)