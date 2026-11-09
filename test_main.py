from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

# Well-known SHA-256 digests, hardcoded so the tests don't reuse the code under test.
HELLO_SHA256 = "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
EMPTY_SHA256 = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"


def test_generate_success():
    """A valid body returns 200 with a JSON checksum field."""
    response = client.post("/generate", json={"text": "hello"})

    assert response.status_code == 200
    assert "checksum" in response.json()


def test_generate_checksum_is_correct():
    """The returned checksum matches the known SHA-256 of the input."""
    response = client.post("/generate", json={"text": "hello"})

    assert response.json() == {"checksum": HELLO_SHA256}


def test_generate_accepts_empty_string():
    """An empty string is valid input and hashes to the known empty digest."""
    response = client.post("/generate", json={"text": ""})

    assert response.status_code == 200
    assert response.json() == {"checksum": EMPTY_SHA256}


def test_generate_missing_text_returns_422():
    """Omitting the required text field fails validation."""
    response = client.post("/generate", json={})

    assert response.status_code == 422
