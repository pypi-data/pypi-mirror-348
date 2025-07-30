import pytest
from fastapi.testclient import TestClient
from app.api import app

client = TestClient(app)

def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"

def test_balance(monkeypatch):
    monkeypatch.setattr("app.web3utils.get_balance", lambda addr: 42)
    resp = client.get("/balance/0x123")
    assert resp.status_code == 200
    assert resp.json()["balance"] == 42 