"""
Contains Network logic including Node and Network classes.
"""

from mockchain.wallet import Wallet
from mockchain.blockchain import Blockchain
from mockchain.transactionpool import TransactionPool


class Network:
    """Defines details of a network where we imagine a set of nodes interacting.

    For example, the mining difficulty is set by the network.
    """
    def __init__(self, difficulty=1):
        self.difficulty = difficulty

    def print_network_data(self, node):
        info = 'NETWORK INFO (at block height ' + str(node.get_block_count) + ')'
        print('\n' + str('=' * len(info)))
        print('' + info)
        print('=' * len(info))
        print('Blockcount    : ' + str(node.get_block_count))
        print('Mempool depth : ' + str(node.get_mempool_count))


class Node:
    def __init__(self, name):
        """
        We can create a new Node which holds it's own wallet,
        a view of the blockchain, and the mempool (transaction pool).
        """
        self.name = name
        self._wallet = Wallet()
        self._blockchain = Blockchain()
        self._transaction_pool = TransactionPool()

    @property
    def wallet_id(self):
        """The ID of the wallet associated with this node."""
        return self._wallet.identity

    @property
    def get_block_count(self):
        return str(self._blockchain.block_count)

    @property
    def get_mempool_count(self):
        return str(self._transaction_pool.get_transaction_count)

    def sign_transaction(self, transaction):
        """Sign a transaction"""
        self._wallet.sign_transaction(transaction)

    def add_transaction_to_mempool(self, transaction):
        self._transaction_pool.append_transaction(transaction)

    def generate_block(self, block, difficulty):
        from mockchain.mining import Mining
        return Mining.generate_block(self._transaction_pool, block, difficulty)

    def append_block(self, block):
        self._blockchain.append_block(block)

    def validate_entire_blockchain(self, validate_signatures=True):
        self._blockchain.validate_entire_blockchain(validate_signatures)

    def print_blockchain_data(self, print_transaction_data=True):
        self._blockchain.print_blockchain_data(print_transaction_data)
