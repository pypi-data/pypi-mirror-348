from web3 import Web3

class SoniaBlockchain:
    def __init__(self, rpc_url="https://mainnet.base.org"):
        self.w3 = Web3(Web3.HTTPProvider(rpc_url))

    def get_balance(self, address):
        if not self.w3.is_address(address):
            raise ValueError("Invalid address")
        balance = self.w3.eth.get_balance(address)
        return self.w3.from_wei(balance, "ether")

    def get_transaction_count(self, address):
        if not self.w3.is_address(address):
            raise ValueError("Invalid address")
        return self.w3.eth.get_transaction_count(address)