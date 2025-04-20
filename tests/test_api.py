import sys
import os
import base64
import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient

# Ensure the parent directory is in the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import app

client = TestClient(app)

CLIENT_ID = "testuser"
CLIENT_SECRET = "testuser"


def get_basic_auth_header():
    credentials = f"{CLIENT_ID}:{CLIENT_SECRET}"
    encoded = base64.b64encode(credentials.encode()).decode()
    return {"Authorization": f"Basic {encoded}"}


def get_bearer_token():
    response = client.post("/token", headers=get_basic_auth_header())
    assert response.status_code == 200
    return response.json()["access_token"]


def get_auth_header():
    token = get_bearer_token()
    return {"Authorization": f"Bearer {token}"}


#Auth tests

def test_token_success():
    response = client.post("/token", headers=get_basic_auth_header())
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_token_invalid_credentials():
    wrong_credentials = base64.b64encode("wrong:creds".encode()).decode()
    response = client.post("/token", headers={"Authorization": f"Basic {wrong_credentials}"})
    assert response.status_code == 401


#News API test

@patch("app.utils.fetch_news")
def test_get_all_news(mock_fetch_news):
    mock_fetch_news.return_value = {
        "totalResults": 2,
        "articles": [
            {"title": "News A", "description": "desc", "url": "http://a.com", "publishedAt": "2025-04-18T10:00:00Z"},
            {"title": "News B", "description": "desc", "url": "http://b.com", "publishedAt": "2025-04-18T10:00:00Z"}
        ]
    }
    response = client.get("/news?skip=0&limit=10&query=test", headers=get_auth_header())
    assert response.status_code == 200
    assert "articles" in response.json()


@patch("app.utils.fetch_news")
def test_save_latest_news(mock_fetch_news):
    mock_fetch_news.return_value = {
        "articles": [
            {"title": "A", "description": "desc", "url": "http://1.com", "publishedAt": "2025-04-18T10:00:00Z"},
            {"title": "B", "description": "desc", "url": "http://2.com", "publishedAt": "2025-04-18T10:00:00Z"},
            {"title": "C", "description": "desc", "url": "http://3.com", "publishedAt": "2025-04-18T10:00:00Z"}
        ]
    }
    response = client.post("/news/save-latest", json={"country_code": "us"}, headers=get_auth_header())
    assert response.status_code == 200
    assert "Saved" in response.json()["message"]


@patch("app.utils.fetch_news")
def test_get_headlines_by_country(mock_fetch_news):
    mock_fetch_news.return_value = {"articles": [], "totalResults": 0}
    response = client.get("/news/headlines/country/us", headers=get_auth_header())
    assert response.status_code == 200
    assert "articles" in response.json() or response.json() == {}


@patch("app.utils.fetch_news")
def test_get_headlines_by_source(mock_fetch_news):
    mock_fetch_news.return_value = {"articles": [], "totalResults": 0}
    response = client.get("/news/headlines/source/cnn", headers=get_auth_header())
    assert response.status_code == 200
    assert "articles" in response.json() or response.json() == {}


@patch("app.utils.fetch_news")
def test_headlines_filter(mock_fetch_news):
    mock_fetch_news.return_value = {
        "articles": [
            {"source": {"id": "cnn"}, "title": "CNN", "description": "desc", "url": "http://cnn.com", "publishedAt": "2025-04-18T10:00:00Z"},
            {"source": {"id": "bbc"}, "title": "BBC", "description": "desc", "url": "http://bbc.com", "publishedAt": "2025-04-18T10:00:00Z"}
        ],
        "totalResults": 2
    }
    response = client.get("/news/headlines/filter?country=us&source=cnn", headers=get_auth_header())
    assert response.status_code == 200
    filtered = response.json()["articles"]
    assert all(article["source"]["id"] == "cnn" for article in filtered)
