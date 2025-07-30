from fastapi import FastAPI
from app.web3utils import get_balance

app = FastAPI()

@app.get("/health")
def health():
    """Health check endpoint."""
    return {"status": "ok"}

@app.get("/balance/{address}")
def balance(address: str):
    """Get ETH balance for an address."""
    bal = get_balance(address)
    return {"address": address, "balance": bal}

@app.post("/strategy/execute")
def execute_strategy(strategy_name: str):
    """Stub for executing a strategy by name."""
    # TODO: Implement strategy execution logic
    return {"strategy": strategy_name, "status": "executed (stub)"} 