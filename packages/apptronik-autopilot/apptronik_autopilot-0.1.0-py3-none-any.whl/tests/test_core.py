import pytest
from app.core import Vault, PortfolioEngine

def test_vault_init():
    v = Vault('0x123')
    assert v.address == '0x123'

def test_vault_methods():
    v = Vault('0x123')
    assert v.deposit(1) is None
    assert v.withdraw(1) is None

def test_portfolio_engine_init():
    v = Vault('0x123')
    pe = PortfolioEngine(v)
    assert pe.vault is v

def test_portfolio_engine_optimize():
    v = Vault('0x123')
    pe = PortfolioEngine(v)
    assert pe.optimize() is None 