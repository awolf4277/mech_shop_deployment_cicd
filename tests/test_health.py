import json

def test_health(client=None):
    from app import app as flask_app
    test_client = flask_app.test_client()
    res = test_client.get("/health")
    assert res.status_code == 200
    data = res.get_json()
    assert data.get("ok") is True
