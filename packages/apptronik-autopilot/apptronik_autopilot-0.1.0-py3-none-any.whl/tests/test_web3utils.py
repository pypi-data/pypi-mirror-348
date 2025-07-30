import os
import pytest
from unittest.mock import patch, MagicMock
from app import web3utils

def test_get_web3_env_missing(monkeypatch):
    monkeypatch.delenv('RPC_ENDPOINT', raising=False)
    with pytest.raises(ValueError):
        web3utils.get_web3()

def test_get_web3_env_present(monkeypatch):
    monkeypatch.setenv('RPC_ENDPOINT', 'http://localhost:8545')
    w3 = web3utils.get_web3()
    assert w3 is not None

@patch('app.web3utils.get_web3')
def test_get_balance_success(mock_get_web3):
    mock_w3 = MagicMock()
    mock_w3.eth.get_balance.return_value = 12345
    mock_get_web3.return_value = mock_w3
    assert web3utils.get_balance('0x123') == 12345

@patch('app.web3utils.get_web3')
def test_get_balance_error(mock_get_web3):
    mock_w3 = MagicMock()
    mock_w3.eth.get_balance.side_effect = Exception('fail')
    mock_get_web3.return_value = mock_w3
    assert web3utils.get_balance('0x123') is None 