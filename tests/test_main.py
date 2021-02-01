from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


# URL + Shortcode provided test
def test_post_shorten():
    response = client.post("/shorten?shortcode=ewx123",
                           json={"url": "https://www.energyworx.com/"})
    assert response.status_code == 201
    assert response.json() == {
        "original_url": "https://www.energyworx.com/",
        "shortcode": "ewx123"
    }


# Only URL provided, generate shortcode
def test_generate_shortcode():
    response = client.post("/shorten",
                           json={"url": "https://www.starlette.io/"})
    assert response.status_code == 201


# No URL provided
def test_no_url():
    response = client.post("/shorten",
                           json={"url": ""})
    assert response.status_code == 400
    assert response.json() == {
        "detail": "URL not present"
    }


# Shortcode already in use
def test_shortcode_exists():
    response = client.post("/shorten?shortcode=ewx123",
                           json={"url": "https://www.google.com/"})
    assert response.status_code == 409
    assert response.json() == {
        "detail": "Shortcode already in use"
    }


# Invalid shortcode length
def test_shortcode_length():
    response = client.post("/shorten?shortcode=ewx123456",
                           json={"url": "https://requests.readthedocs.io/en/master/"})
    assert response.status_code == 412
    assert response.json() == {
        "detail": "The provided shortcode is invalid (Length of shortcode should be 6)"
    }


# Request shortcode
def test_request_shortcode():
    response = client.get("/ewx123")
    assert response.status_code == 302
    assert response.json() == {
        "location": "https://www.energyworx.com/"
    }


# Request inexistent shortcode
def test_bad_shortcode():
    response = client.get("/ewx124")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Shortcode not found"
    }


# Request shortcode stats
def test_shortcode_stats():
    response = client.get("/ewx123/stats")
    assert response.status_code == 200


# Request inexistent shortcode stats
def test_shortcode_stats():
    response = client.get("/ewx124/stats")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Shortcode not found"
    }
