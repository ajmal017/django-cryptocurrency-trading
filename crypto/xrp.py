import requests
import json

from cadmin import models
from .models import XRP
from eth_account import Account as eaAccount
# from django.core import serializers
from ripple_api import RippleRPCClient
from ripple.sign import sign_transaction, create_signing_hash

# RIPPLE_SERVER = 'http://r.ripple.com:51235/' # local
RIPPLE_SERVER = 'http://s.altnet.ripple.com:51235/' # testnet local
# RIPPLE_SERVER = 'http://s1.ripple.com:51234/' # public
# RIPPLE_SERVER = 'https://s.altnet.rippletest.net:51234/' # testnet public


class XRPProcessor:
    def __init__(self, customer):
        self.customer = customer#models.Customers.objects.get(id=1) #customer
        if self.customer.xrp_wallet() is None:
            self.wallet_generation()
        self.password = self.customer.btc_wallet().password
        self.addr = self.customer.xrp_wallet().addr
        self.client = RippleRPCClient(RIPPLE_SERVER)#, username='<username>', password='<password>'

    def wallet_generation(self, label = None):
        label = label if label is not None else self.customer.user.get_fullname() + ' wallet'
        user_password = get_random_string(60)
        acct = self.client.wallet_propose(passphrase = user_password)
        # acct = json.loads(requests.post('https://faucet.altnet.rippletest.net/accounts').content)['account']
        xrp_wallet = XRP(
            id = acct['account_id'],
            addr = acct['address'],
            label = label,
            customer = self.customer,
            secret = acct['secret'],
            password = user_password
        )
        xrp_wallet.save()
        return acct

    def wallet_info(self):
        account_info = self.client.account_info(self.addr)
        return account_info

    def get_balance(self):
        get_balance = self.wallet_info()['account_data']['Balance']
        obj, created = models.Balance.objects.get_or_create(customer=self.customer, currency='XRP')
        obj.amount = get_balance
        obj.save()
        return get_balance

    def account_lines(self):
        return self.client.account_lines(self.addr)

    def account_channels(self, destination_addr):
        return self.client.account_channels(self.addr, destination_addr)

    def account_currencies(self):
        return self.client.account_currencies(self.addr)

    def account_objects(self):
        return self.client.account_objects(self.addr)

    def account_offers(self):
        return self.client.account_offers(self.addr)

    def account_tx(self):
        return self.client.account_tx(self.addr)

    def gateway_balances(self):
        return self.client.gateway_balances(self.addr)

    def gateway_balances(self):
        return self.client.gateway_balances(self.addr)

    def noripple_check(self):
        return self.client.noripple_check(self.addr)

    def ledger(self):
        return self.client.ledger()

    def ledger_closed(self):
        return self.client.ledger_closed()

    def ledger_current(self):
        return self.client.ledger_current()

    def ledger_data(self, ledger_hash):
        return self.client.ledger_data(ledger_hash)

    def ledger_entry(self):
        return self.client.ledger_entry()

    def sign(self, tx_json, secret=""):
        return self.client.sign(tx_json, secret, True)

    def sign_for(self, account, seed, key_type, tx_json):
        return self.client.sign_for(self.addr, seed, key_type, tx_json)

    def submit(self, tx_blob):
        return self.client.ledger_current(tx_blob)

    def tx_history(self):
        return self.client.tx_history()

    # def get_balance_multi(self):
    #     get_balances = self.client.get_balance_multiple()
    #     return get_balances

    def send_tx(self, target_addr, amount, currency = "USD", secret = None):
        secret = secret if secret is not None else self.customer.xrp_wallet().secret
        transaction = {
            'TransactionType': "TrustSet",
            'Account': self.addr,
            'Destination': target_addr,
            'Amount' : {
                "currency" : currency,
                "value" : 1,
                "issuer" : self.addr
            }
        }
        tx_hash = self.sign(transaction)
        # return tx_hash
        payment = self.submit(tx_hash['TxnSignature'])
        return payment

    def tx_fee(self):
        return self.client.fee()

    def get_target_wallet_addr(self, customer=None, email=None):
        if customer is not None:
            return customer.xrp_wallet().addr
        if email is not None:
            user = models.Users.objects.get(email=email)
            return user.customer().xrp_wallet().addr
        return None