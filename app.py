
import os
import sqlite3
from contextlib import closing

from flask import Flask, abort, jsonify, render_template, request, url_for

from data import MEMES, QUESTIONS, TRAITS
from scoring import calculate

PUBLIC_MEME_FIELDS = ("name", "emoji", "tagline", "description", "color", "accent")


def public_meme(meme_id):
    m = MEMES[meme_id]
    image = url_for("static", filename=f"memes/{m['image']}") if m.get("image") else None
    return {"id": meme_id, "image": image, **{k: m[k] for k in PUBLIC_MEME_FIELDS}}


def create_app(db_path=None):
    app = Flask(__name__)
    app.json.ensure_ascii = False  # нормальна кирилиця в JSON
    app.config["DB_PATH"] = db_path or os.path.join(app.instance_path, "stats.db")
    os.makedirs(os.path.dirname(app.config["DB_PATH"]), exist_ok=True)

    def db():
        return closing(sqlite3.connect(app.config["DB_PATH"]))

    with db() as conn, conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS results ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, meme_id TEXT NOT NULL, "
            "created_at TEXT DEFAULT CURRENT_TIMESTAMP)"
        )

    def stats():
        with db() as conn:
            rows = conn.execute("SELECT meme_id, COUNT(*) FROM results GROUP BY meme_id").fetchall()
        counts = {mid: 0 for mid in MEMES}
        counts.update(dict(rows))
        return counts, sum(counts.values())

    def rarity(meme_id):
        counts, total = stats()
        return {"count": counts[meme_id], "total": total,
                "percent": round(counts[meme_id] / total * 100, 1) if total else 0}

    @app.get("/")
    def index():
        return render_template("index.html", preload=None)

    @app.get("/result/<meme_id>")
    def shared_result(meme_id):
        if meme_id not in MEMES:
            abort(404)
        return render_template("index.html", preload=meme_id, meme=public_meme(meme_id))

    @app.get("/api/questions")
    def api_questions():
        return jsonify({
            "traits": TRAITS,
            "questions": [
                {"id": q["id"], "text": q["text"],
                 "options": [{"id": i, "text": o["text"]} for i, o in enumerate(q["options"])]}
                for q in QUESTIONS
            ],
        })

    @app.post("/api/submit")
    def api_submit():
        payload = request.get_json(silent=True) or {}
        try:
            ranking, traits = calculate(payload.get("answers"))
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        winner = ranking[0]["id"]
        with db() as conn, conn:
            conn.execute("INSERT INTO results (meme_id) VALUES (?)", (winner,))
        return jsonify({
            "result": {**public_meme(winner), "percent": ranking[0]["percent"]},
            "ranking": [{**public_meme(r["id"]), "percent": r["percent"]} for r in ranking],
            "traits": traits,
            "rarity": rarity(winner),
        })

    @app.get("/api/meme/<meme_id>")
    def api_meme(meme_id):
        if meme_id not in MEMES:
            return jsonify({"error": "Мем не знайдено"}), 404
        return jsonify({"result": public_meme(meme_id), "rarity": rarity(meme_id)})

    @app.get("/api/stats")
    def api_stats():
        counts, total = stats()
        return jsonify({"total": total, "memes": [
            {**public_meme(mid), "count": c, "percent": round(c / total * 100, 1) if total else 0}
            for mid, c in sorted(counts.items(), key=lambda x: -x[1])
        ]})

    @app.errorhandler(404)
    def not_found(_):
        if request.path.startswith("/api/"):
            return jsonify({"error": "Не знайдено"}), 404
        return render_template("index.html", preload=None), 404

    return app


if __name__ == "__main__":
    create_app().run(debug=True)
