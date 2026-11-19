from fastapi.testclient import TestClient
from sklearn.datasets import load_breast_cancer

from app import app

client = TestClient(app)


def test_predict_returns_probability_in_range():
    features = load_breast_cancer().data[0].tolist()
    r = client.post("/predict", json={"features": features})
    assert r.status_code == 200
    body = r.json()
    assert 0 <= body["risk"] <= 1
    assert body["label"] in ("higher", "lower")


def test_predict_rejects_wrong_length():
    r = client.post("/predict", json={"features": [1.0] * 29})
    assert r.status_code == 422


def test_home_page_shows_live_example_score():
    r = client.get("/")
    assert r.status_code == 200
    assert "Risk model service" in r.text
    assert "__RISK__" not in r.text and "__PCT__" not in r.text


def test_health():
    assert client.get("/health").json() == {"status": "ok"}
