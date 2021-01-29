from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


# URL + Shortcode provided test
def test_post_shorten():
    response = client.post("/shorten",
                           body={""},
                           json={"url": "https://www.energyworx.com/",
                                 "shortcode": "ewx123"})
    assert response.status_code == 201
    assert response.json() == {
        "original_url": "https://www.energyworx.com/",
        "shortcode": "ewx123"
    }

# Only URL provided, generate shortcode


# No URL provided, shortcode provided


# Request shortcode


# Request inexistent shortcode


# Request shortcode stats


# Request inexistent shortcode stats
