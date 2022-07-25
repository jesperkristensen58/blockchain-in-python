"""
Define a block and its logic.

@author Jesper Kristensen
"""
from mockchain.utils import Utils


class Block:
    """Represent a block in the blockchain"""

    def __init__(self):
        """Initialize a block"""
        self._transactions = []  # list of transactions in this block
        self._previous_block_hash = None  # I point to a previous block
        self._nonce = None  # the nonce I found when solving the mining puzzle
        self._height = 0  # which height I am in the blockchain
        self._difficulty = 0  # TODO BONUS: Implement difficulty as the real hexadecimal base/exponent formula
        self._block_hash = None  # my own block hash

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, new_height):
        self._height = new_height

    @property
    def nonce(self):
        return self._nonce

    @nonce.setter
    def nonce(self, nonce):
        self._nonce = nonce

    @property
    def difficulty(self):
        return self._difficulty

    @difficulty.setter
    def difficulty(self, difficulty):
        self._difficulty = difficulty

    @property
    def transactions(self):
        """Return the list of transactions in this block"""
        return self._transactions

    @property
    def previous_block_hash(self):
        """Return the previous block hash"""
        return self._previous_block_hash

    @previous_block_hash.setter
    def previous_block_hash(self, new_previous_block_hash):
        self._previous_block_hash = new_previous_block_hash

    @property
    def block_hash(self):
        """Get the block hash of this block"""
        if self._block_hash is None:
            self.recompute_block_hash()  # we don't have a hash; so derive it
        
        return self._block_hash

    def recompute_block_hash(self):
        """Force a recalculation of the block hash - used during mining"""
        if self.nonce is None:
            raise Exception('You must set a valid nonce before trying to derive the block_hash')

        block_data = self.get_block_data_as_string

        self._block_hash = Utils.sha256(block_data)
        return self._block_hash

    def append_transaction(self, transaction):
        if Utils.verify_signature(transaction.signature, transaction.pub_key, transaction.unsigned_to_string):
            self._transactions.append(transaction)
        else:
            raise Exception("Cannot add transaction, invalid signature")

    @property
    def get_txs_string(self):
        """Convert all transactions in this block into one single string."""
        txs_string = ""
        for transaction in self._transactions:
            txs_string += transaction.unsigned_to_string
        
        return txs_string

    @property
    def tx_count(self):
        """The number of transactions in this block"""
        return len(self._transactions)

    @property
    def get_block_data_as_string(self):
        """Represent the details of this block as a string"""

        prev_block_hash = self.previous_block_hash  # importantly, the previous block hash is
                                                    # cemented into this block's hash
        transactions = self.get_txs_string
        difficulty_target = self.difficulty
        nonce = self.nonce

        block_string = prev_block_hash + transactions + str(difficulty_target) + str(nonce)
        return block_string

    def print_transaction_ids(self):
        """Print the ids of transactions in this block"""
        print("  Transactions in block " + str(self.height) + ":")
        for transaction in self._transactions:
            print("    " + transaction.tx_id)
