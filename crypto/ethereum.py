import os.path
from web3 import Web3


class EthereumProcessor:
    """
    Class used for bringing together the Ethereum operations
    """

    def __init__(self, ipc_file):
        provider = Web3.IPCProvider(os.path.abspath(ipc_file))
        self.w3 = Web3(provider)

    def version(self):
        return self.w3.geth.clientVersion

    def create_wallet(self, password):
        return self.w3.geth.personal.newAccount(password)

    def open_wallet(self, account, password, duration=None):
        return self.w3.geth.personal.unlockAccount(account, password, duration)

    def close_wallet(self, account):
        return self.w3.geth.personal.lockAccount(account)

    def get_all_accounts(self):
        return self.w3.geth.personal.listAccounts()

    def get_balance(self, account):
        return self.w3.eth.getBalance(account)
