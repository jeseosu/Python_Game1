
import math

from data import MEMES, QUESTIONS, TRAITS

_Q_BY_ID = {q["id"]: q for q in QUESTIONS}


def _max_per_trait():

    return {
        t: sum(max(o["w"].get(t, 0) for o in q["options"]) for q in QUESTIONS) or 1
        for t in TRAITS
    }


def validate(answers):

    if not isinstance(answers, list) or len(answers) != len(QUESTIONS):
        raise ValueError("Потрібно відповісти на всі питання")
    seen = set()
    for a in answers:
        if not isinstance(a, dict):
            raise ValueError("Некоректний формат відповіді")
        q, o = a.get("q"), a.get("o")
        if q not in _Q_BY_ID or q in seen:
            raise ValueError("Невідоме або повторене питання")
        if not isinstance(o, int) or isinstance(o, bool) or not 0 <= o < len(_Q_BY_ID[q]["options"]):
            raise ValueError("Невідомий варіант відповіді")
        seen.add(q)


def calculate(answers):

    validate(answers)
    user = dict.fromkeys(TRAITS, 0)
    for a in answers:
        for trait, w in _Q_BY_ID[a["q"]]["options"][a["o"]]["w"].items():
            user[trait] += w

    u_norm = math.sqrt(sum(v * v for v in user.values())) or 1
    ranking = []
    for meme_id, m in MEMES.items():
        p = m["profile"]
        dot = sum(user[t] * p[t] for t in TRAITS)
        p_norm = math.sqrt(sum(v * v for v in p.values())) or 1
        cos = dot / (u_norm * p_norm)
        ranking.append({"id": meme_id, "score": cos, "percent": round(cos ** 2 * 100)})
    ranking.sort(key=lambda r: (-r["score"], r["id"]))

    mx = _max_per_trait()
    traits = {t: round(user[t] / mx[t] * 100) for t in TRAITS}
    return ranking, traits
