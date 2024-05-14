

def test_healthcheck(test_app):
    response = test_app.get("/healthcheck")
    assert response.status_code == 200
    assert response.json() == "working!"


