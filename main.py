"""
This is the Python Mockchain.

An educational tool implemented to teach you basic concepts of a Blockchain.
We use Python for its fast easy development capabilities.

# TODO: Implement the concept of UTXOs and Coinbase transactions (block reward = block subsidy + fees)

@author Jesper Kristensen
"""

from mockchain.utils import Utils
from mockchain.network import Network, Node
from mockchain.transaction import Transaction
from mockchain.block import Block

print("""                                                                  
 _____     _   _              _____         _       _       _     
|  _  |_ _| |_| |_ ___ ___   |     |___ ___| |_ ___| |_ ___|_|___ 
|   __| | |  _|   | . |   |  | | | | . |  _| '_|  _|   | .'| |   |
|__|  |_  |_| |_|_|___|_|_|  |_|_|_|___|___|_,_|___|_|_|__,|_|_|_|
      |___|

Enjoy running the Python Mockchain!""")

# Create two node instances that we will use to send and receive our imagined
# blockchain coins, they will also function as miners
node_1 = Node('Alice Node')
node_2 = Node('Bob Node')

# The network difficulty defines how many leading zeros a block hash must have
# for it to be considered valid
network = Network(difficulty=2)

# Create genesis block with one transaction that pays mining reward to Bob

# We don't have the concept of a utxo set in this example code yet so we allow
# spends from any wallet, even if it doesn't hold any coins
t = Transaction(
    sender=node_1.wallet_id,  # Sender is a pub key hash
    recipient=Utils.base58encode(node_2.wallet_id),
    value = 50.0
)

# The sender needs to sign the transaction using their private key
node_1.sign_transaction(t)

# The signed transaction is added to the mempool - a collection of transactions
# waiting to be added to a block
node_1.add_transaction_to_mempool(t)

# To view a transaction's data:
t.print_transaction_data()

# We need a dummy block that we can use to provide the 'previous block hash'
# value for our genesis block
block = Block()
block._block_hash = Utils.sha256('Chancellor on brink of second bailout for banks')

# Create the genesis block by mining at the current network difficulty
# Adding transactions to a block should remove them from the mempool
block = node_1.generate_block(block, network.difficulty)

# Append the valid block to the node's copy of the blockchain
node_1.append_block(block)

# Create some more transactions ready to be added to a new block. Each
# transaction needs to be signed by the sender's wallet using the id,
# which is a base64 encoded public key

t = Transaction(
    sender=node_2.wallet_id,
    recipient=Utils.base58encode(node_1.wallet_id),
    value = 2
)
node_2.sign_transaction(t)
node_1.add_transaction_to_mempool(t)
block = node_1.generate_block(block, network.difficulty)
node_1.append_block(block)

# Increase the network difficulty to show how it affects block mining and
# the resulting block hash that is found
network.difficulty += 1

block = node_1.generate_block(block, network.difficulty)
node_1.append_block(block)

# To view the transactions in a block:
block.print_transaction_ids()

# View the 'network' data for a given node's view
network.print_network_data(node_1)

# Validate the blockchain - including transaction signatures
node_1.validate_entire_blockchain()

# To view a node's blockchain data (including tx data):
node_1.print_blockchain_data(True)
