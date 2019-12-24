from mnemonic import Mnemonic
import os
import grpc
import logging
from crypto.api_pb2_grpc import WalletServiceStub, WalletLoaderServiceStub, VersionServiceStub
import crypto.api_pb2 as req
from base64 import b64encode

logger = logging.getLogger('raplev')
logger.setLevel(logging.INFO)


class UsernamePasswordCallCredentials(grpc.AuthMetadataPlugin):
    """Metadata wrapper for raw access token credentials."""

    def __init__(self, username, password):
        """

        """
        self._username = username
        self._password = password

    def __call__(self, context, callback):
        credentials = "{}:{}".format(self._username, self._password).encode()
        basic_auth = "Basic {}".format(b64encode(credentials).decode('ascii'))
        metadata = (('authorization', basic_auth),)
        callback(metadata, None)


class BitcoinProcessor:
    """Class used for defining Bitcoin operations

    The class uses gRPC API with btcwallet to access the bitcoin wallets and perform transactions
    :param hostname: The hostname to which to connect
    :param port: Port number
    :param username: Defined in btcwallet.conf. Usually the same username that is used to connect to the btcd API
    :param password: Defined in btcwallet.conf. Usually the same password that is used  to connect to the btcd API
    """

    def __init__(
            self, hostname, port, username, password,
            secure=True,
            ca_path='/data/btc/.btcwallet/ec-ca.crt',
            cert_path='/data/btc/.btcwallet/client.cert',
            key_path='/data/btc/.btcwallet/client.key'
    ):
        self.http_credentials = grpc.metadata_call_credentials(
            UsernamePasswordCallCredentials(username, password))
        if secure:
            certs = [os.path.abspath(ca_path), os.path.abspath(key_path), os.path.abspath(cert_path)]
            cert_data = list()
            for file in certs:
                with open(file, 'rb') as f:
                    cert_data.append(f.read())
            creds = grpc.ssl_channel_credentials(cert_data[0], cert_data[1], cert_data[2])
            self.ic = grpc.secure_channel(hostname+':'+str(port), creds)
        else:
            self.ic = grpc.insecure_channel(hostname+":"+str(port))

    def __del__(self):
        self.ic.close()

    def version(self):
        """Gets the API version

        :return: The response from the gRPC API with the corresponding version description
        """
        stub = VersionServiceStub(self.ic)
        try:
            response = stub.Version.with_call(req.VersionRequest(), credentials=self.http_credentials)
        except grpc.RpcError as e:
            logger.info('Version failed with {0}: {1}'.format(e.code(), e.details()))
            return None
        return response

    def wallet_exists(self):
        """Used to find out if a wallet has already been created or not in the current directory

        :return: The response from the gRPC API with the corresponding boolean variable, describing if the wallet exists
        """
        stub = WalletLoaderServiceStub(self.ic)
        try:
            response = stub.WalletExists.with_call(req.WalletExistsRequest(), credentials=self.http_credentials)
        except grpc.RpcError as e:
            logger.info('WalletExists failed with {}: {}'.format(e.code(), e.details()))
            return None
        return response

    def create_wallet(self, private_passphrase, public_passphrase='', seed=None, mnemonic=None):
        """Creates a Bitcoin wallet

        When called only with the private passphrase as the argument, generates a new mnemonic phrase and creates new
        wallet. Can also be called with a pre-existing mnemonic phrase or bitcoin seed to access pre-existing wallet

        :param private_passphrase: The password used for creating new wallet / initializing pre-existing wallet
        :param public_passphrase: Password used for protecting public data. If empty, a weak default will be used
        :param seed: A BIP0032 Bitcoin wallet seed
        :param mnemonic: A BIP0039 wallet mnemonic. Must have 12, 15, 18, 21 or 24 words

        :return: API response is wallet successfully created or None in case of failure
        """
        stub = WalletLoaderServiceStub(self.ic)
        m = Mnemonic('english')
        if mnemonic:
            if m.check(mnemonic):
                seed = m.to_seed(mnemonic, private_passphrase)
            else:
                return None
        elif seed is None:
            m = Mnemonic('english')
            mnemonic = m.generate()
            if not m.check(mnemonic):
                # Mnemonic hasn't been generated correctly
                return None
            seed = m.to_seed(mnemonic, private_passphrase)
        message = req.CreateWalletRequest(
            public_passphrase=public_passphrase.encode('utf-8'),
            private_passphrase=private_passphrase.encode('utf-8'),
            seed=seed
        )
        try:
            response = stub.CreateWallet.with_call(message, credentials=self.http_credentials)
        except grpc.RpcError as e:
            logger.info('CreateWallet failed with {0}: {1}'.format(e.code(), e.details()))
            return None
        else:
            logger.info("Wallet created:", response)
            return {'response': response, 'mnemonic': mnemonic}

    def open_wallet(self, public_passphrase=''):
        """Opens a pre-existing wallet

        :param public_passphrase: The public passphrase. If its length is zero, an insecure default is used instead.
        :return: OpenWalletResponse if successful and None in case of error
        """
        stub = WalletLoaderServiceStub(self.ic)
        message = req.OpenWalletRequest(
            public_passphrase=public_passphrase.encode('utf-8')
        )
        try:
            response = stub.OpenWallet.with_call(message, credentials=self.http_credentials)
        except grpc.RpcError as e:
            logger.info('OpenWallet failed with {0}: {1}'.format(e.code(), e.details()))
            return None
        else:
            logger.info("Wallet opened:", response)
            return response

    def close_wallet(self):
        """Closes the opened wallet

        :return: CloseWalletResponse if successful and None in case of error
        """
        stub = WalletLoaderServiceStub(self.ic)
        try:
            response = stub.CloseWallet.with_call(req.CloseWalletRequest(), credentials=self.http_credentials)
        except grpc.RpcError as e:
            logger.info('CloseWallet failed with {0}: {1}'.format(e.code(), e.details()))
            return None
        else:
            logger.info("Wallet closed:", response.user.username)
            return response

    def get_all_accounts(self):
        """Returns all the accounts used by the wallet

        :return: AccountsResponse if successful and None in case of error
        """
        stub = WalletServiceStub(self.ic)
        try:
            response = stub.Accounts(req.AccountsRequest())
        except grpc.RpcError as e:
            logger.info('Accounts failed with {0}: {1}'.format(e.code(), e.details()))
        else:
            return response

    def next_address(self):
        """Returns the next address to which to send the currency

        :return: NextAccountResponse if successful and None in case of error
        """
        stub = WalletServiceStub(self.ic)
        try:
            response = stub.NextAddress.with_call(req.NextAccountRequest(), credentials=self.http_credentials)
        except grpc.RpcError as e:
            logger.info('NextAddress failed with {0}: {1}'.format(e.code(), e.details()))
            return None
        return response

    def get_balance(self, account_number, required_confirmations):
        """Gets the current wallet's balance

        :param account_number: The account number to query, starting with zero
        :param required_confirmations: The number of confirmations required. If 1, only the local btcd server is used
        :return BalanceResponse if successful and None in case of error:
        """
        stub = WalletServiceStub(self.ic)
        message = req.BalanceRequest(
            account_number=account_number,
            required_confirmations=required_confirmations
        )
        try:
            response = stub.Balance.with_call(message, credentials=self.http_credentials)
        except grpc.RpcError as e:
            logger.info('Balance failed with {0}: {1}'.format(e.code(), e.details()))
            return None
        else:
            return response
