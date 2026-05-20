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
    power INTEGER,
    energy INTEGER
)
""")
conn.commit()

# ================= HOME =================
@app.route("/")
def home():
    return "🚀 BTC Clicker Server Running"

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
            "power": 1,
            "energy": 100
        })

    return jsonify({
        "id": row[0],
        "name": row[1],
        "coins": row[2],
        "power": row[3],
        "energy": row[4]
    })

# ================= SAVE =================
@app.route("/save", methods=["POST"])
def save():
    data = request.json

    user_id = str(data["id"])
    name = data.get("name", "unknown")
    coins = int(data.get("coins", 0))
    power = int(data.get("power", 1))
    energy = int(data.get("energy", 100))

    cur.execute("""
    INSERT OR REPLACE INTO users VALUES (?, ?, ?, ?, ?)
    """, (user_id, name, coins, power, energy))

    conn.commit()

    return jsonify({"ok": True})

# ================= TAP SYSTEM =================
@app.route("/tap", methods=["POST"])
def tap():
    data = request.json
    uid = str(data["id"])

    cur.execute("SELECT coins, power, energy FROM users WHERE id=?", (uid,))
    row = cur.fetchone()

    if not row:
        coins, power, energy = 0, 1, 100
    else:
        coins, power, energy = row

    # ❌ нет энергии → нельзя тапать
    if energy <= 0:
        return jsonify({"ok": False, "msg": "no energy", "crit": 0})

    gain = power

    coins += gain
    energy -= 1

    cur.execute("""
        UPDATE users
        SET coins=?, power=power, energy=?
        WHERE id=?
    """, (coins, energy, uid))

    conn.commit()

    return jsonify({
        "ok": True,
        "crit": gain,
        "coins": coins,
        "energy": energy
    })

# ================= SHOP =================
@app.route("/buy", methods=["POST"])
def buy():
    data = request.json
    uid = str(data["id"])
    item = data["item"]

    cur.execute("SELECT coins, power, energy FROM users WHERE id=?", (uid,))
    row = cur.fetchone()

    if not row:
        return jsonify({"ok": False})

    coins, power, energy = row

    if item == "p1" and coins >= 150:
        coins -= 150
        power += 1

    elif item == "p2" and coins >= 400:
        coins -= 400
        power += 2

    elif item == "energy" and coins >= 300:
        coins -= 300
        energy += 50

    cur.execute("""
        UPDATE users
        SET coins=?, power=?, energy=?
        WHERE id=?
    """, (coins, power, energy, uid))

    conn.commit()

    return jsonify({"ok": True})

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
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)