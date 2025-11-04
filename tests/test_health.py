# tests/test_health.py
from flask_app import app as _app

def test_health_route():
    client = _app.test_client()
    res = client.get("/health")
    assert res.status_code == 200
    data = res.get_json()
    assert data.get("ok") is True
