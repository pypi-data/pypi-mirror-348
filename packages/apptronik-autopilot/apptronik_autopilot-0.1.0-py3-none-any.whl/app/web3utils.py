from web3 import Web3
import os

def get_web3():
    """Create a Web3 instance from the RPC endpoint in environment."""
    rpc = os.getenv('RPC_ENDPOINT')
    if not rpc:
        raise ValueError('RPC_ENDPOINT not set in environment')
    return Web3(Web3.HTTPProvider(rpc))

def get_balance(address):
    """Get the ETH balance of an address."""
    w3 = get_web3()
    try:
        return w3.eth.get_balance(address)
    except Exception as e:
        print(f"Error getting balance: {e}")
        return None 