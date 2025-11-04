def test_health():
    from app import app as flask_app
    client = flask_app.test_client()
    r = client.get("/health")
    assert r.status_code == 200
    data = r.get_json()
    assert data.get("ok") is True
