"""

# TODO: BONUS
# Implement UTXO logic so that each TX is dependant on a previous TX
# and each TX is locked to a pubkey hash so that only a corresponding pubkey can spend the TX by satisfying the locking script
# You will need to also implement the locking and unlocking script logic from Week 2
"""

import datetime
from mockchain.utils import Utils


class Transaction:
    """A transaction.
    
    A transaction is a transfer of an amount of coins with a given equivalent
    value from a sender to a receiver.
    """

    def __init__(self, sender, recipient, value):
        """Construct a new Transaction object"""
        self._value = value
        self._time = datetime.datetime.now()
        self.sender = sender
        self.recipient = recipient
        self.signature = ''
        self.pub_key = ''

    @property
    def tx_id(self):
        """Return the ID of the transaction as its unique hash."""
        return Utils.sha256(self.unsigned_to_string)

    @property
    def unsigned_to_string(self):
        """Take an unsigned transaction and return a string representation of it."""
        tx_dict = self.to_dict()
        tx_string = tx_dict['sender'] + tx_dict['recipient'] + str(tx_dict['value']) + str(tx_dict['time'])
        return tx_string

    @property
    def signed_to_string(self):
        """Take a signed transaction and return a string representation of it."""
        tx_dict = self.to_dict()
        tx_string = tx_dict['sender'] + tx_dict['recipient'] + str(tx_dict['value']) + str(tx_dict['time']) + tx_dict[
            'signature'] + tx_dict['pub_key']
        return tx_string

    def to_dict(self):
        """Represent this transaction as a dictionary."""
        return {
            'sender': self.sender,
            'recipient': self.recipient,
            'value': self._value,
            'time': self._time,
            'signature': self.signature,
            'pub_key': self.pub_key}

    def print_transaction_data(self):
        tx_dict = self.to_dict()
        print('Sender       : ' + tx_dict['sender'])
        print('Recipient    : ' + tx_dict['recipient'])
        print('Value        : ' + str(tx_dict['value']))
        print('Created      : ' + str(tx_dict['time']))
        print('Signature    : ' + tx_dict['signature'])
        print('Pub key      : ' + tx_dict['pub_key'])
