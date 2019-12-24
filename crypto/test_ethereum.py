#! /usr/bin/env python3

import unittest
from ethereum import EthereumProcessor


class TestEthereum(unittest.TestCase):
    def test_ethereum_connection(self):
        geth_ipc = '/data/eth/.ethereum/testnet/geth.ipc'
        processor = EthereumProcessor(geth_ipc)
        self.assertEqual(processor.w3.isConnected(), True)
        self.assertTrue(processor.version().startswith('Geth'))


if __name__ == '__main__':
    unittest.main()
