
from mockchain.utils import Utils


class TransactionPool:
    """Represent a transaction pool also called a mempool.
    
    Transactions are stored in this pool.
    """

    def __init__(self):
        """Initialize a transaction pool"""
        self._transactions = []  # we keep a list of transactions in the pool

    def append_transaction(self, transaction):
        """
        Append a transaction to the transaction pool aka the mempool.
        """
        if Utils.verify_signature(transaction.signature, transaction.pub_key, transaction.unsigned_to_string):
            self._transactions.append(transaction)
        else:
            raise Exception('Cannot add transaction to mempool - Invalid signature')

    @property
    def get_transactions(self):
        """Return all transactions in the mempool"""
        return self._transactions

    @property
    def get_transaction_count(self):
        """Get the mempool size"""
        return len(self._transactions)

    def remove_transaction(self, transaction):
        """Remove a transaction from the mempool"""
        return self._transactions.remove(transaction)
