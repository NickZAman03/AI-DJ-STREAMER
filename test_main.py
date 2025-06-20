"""
Simple tests for AI DJ Streamer
"""

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "ai-dj-streamer"}

def test_mood_analysis_positive():
    """Test mood analysis with positive text"""
    response = client.post("/mood", json={"text": "I'm so happy today!"})
    assert response.status_code == 200
    data = response.json()
    assert "mood" in data
    assert "suggested_track" in data
    assert data["mood"] in ["happy", "excited"]

def test_mood_analysis_negative():
    """Test mood analysis with negative text"""
    response = client.post("/mood", json={"text": "I'm feeling really sad today."})
    assert response.status_code == 200
    data = response.json()
    assert "mood" in data
    assert "suggested_track" in data
    assert data["mood"] in ["sad", "angry"]

def test_mood_analysis_neutral():
    """Test mood analysis with neutral text"""
    response = client.post("/mood", json={"text": "The weather is okay today."})
    assert response.status_code == 200
    data = response.json()
    assert "mood" in data
    assert "suggested_track" in data
    assert data["mood"] == "neutral"

def test_mood_analysis_empty():
    """Test mood analysis with empty text"""
    response = client.post("/mood", json={"text": ""})
    assert response.status_code == 400

def test_root_endpoint():
    """Test root endpoint serves HTML"""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

if __name__ == "__main__":
    pytest.main([__file__]) 