import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app  # noqa: E402
from data import MEMES, QUESTIONS  # noqa: E402
from scoring import calculate  # noqa: E402


@pytest.fixture
def client(tmp_path):
    return create_app(str(tmp_path / "t.db")).test_client()


def answers(option):
    return [{"q": q["id"], "o": option} for q in QUESTIONS]


def test_questions_hide_weights(client):
    data = client.get("/api/questions").get_json()
    assert len(data["questions"]) == len(QUESTIONS)
    assert "w" not in data["questions"][0]["options"][0]


def test_submit_returns_valid_meme(client):
    r = client.post("/api/submit", json={"answers": answers(0)})
    assert r.status_code == 200
    body = r.get_json()
    assert body["result"]["id"] in MEMES
    assert len(body["ranking"]) == len(MEMES)
    assert body["rarity"]["total"] == 1


@pytest.mark.parametrize("bad", [None, [], [{"q": 1, "o": 99}] * 8, [{"q": 1, "o": 0}] * 8, "x"])
def test_submit_rejects_bad_input(client, bad):
    assert client.post("/api/submit", json={"answers": bad}).status_code == 400


def test_extreme_profiles_pick_expected_memes():
    assert calculate(answers(2))[0][0]["id"] == "gigachad"
    assert calculate(answers(1))[0][0]["id"] == "chill_guy"


def test_shared_page_and_404(client):
    assert client.get("/result/six_seven").status_code == 200
    assert client.get("/result/nope").status_code == 404
    assert client.get("/api/meme/nope").status_code == 404


def test_stats_counts(client):
    client.post("/api/submit", json={"answers": answers(2)})
    s = client.get("/api/stats").get_json()
    assert s["total"] == 1 and s["memes"][0]["id"] == "gigachad"
