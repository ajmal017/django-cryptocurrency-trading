#!/usr/bin/env python3

import unittest
from bitcoin import BitcoinProcessor

host = 'localhost'
port = 18332
rpccert_path = '/data/btc/.btcwallet/rpc.cert'


class MyTestCase(unittest.TestCase):

    def test_btc_version(self):
        processor = BitcoinProcessor(host, port, 'myuser', 'SomeDecentp4ssw0rd')
        self.assertIn('major: 2', str(processor.version()[0]))

    def test_wallet_exists(self):
        processor = BitcoinProcessor(host, port, 'myuser', 'SomeDecentp4ssw0rd')
        self.assertEqual(str(processor.wallet_exists()[0].exists), 'True')


if __name__ == '__main__':
    unittest.main()
