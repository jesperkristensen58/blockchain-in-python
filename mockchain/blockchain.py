"""
Define a Blockchain.

See also mockchain/block.py for how a block looks.
"""
from mockchain.utils import Utils
from mockchain.mining import Mining


class Blockchain:

    def __init__(self):
        """Construct a blockchain"""
        self._blocks = []
        self._utils = Utils()

    @property
    def block_count(self):
        """Number of blocks in the blockchain"""
        return len(self._blocks)

    def append_block(self, block):
        """Append a block to the blockchain"""
        self._blocks.append(block)

    def validate_entire_blockchain(self, validate_signatures=True):
        """Validate the blockchain.
        
        Loop over the blocks and transactions validating them.
        """
        previous_block_hash = ""

        info = "VALIDATING BLOCKCHAIN "
        Utils.log("\n" + str("=" * len(info)))
        Utils.log(info)
        Utils.log("=" * len(info))

        for block in self._blocks:

            Utils.log("Verifying block " + str(block.height))

            # Genesis block check
            if block.height == 1:
                previous_block_hash = Utils.sha256("Chancellor on brink of second bailout for banks")
            
            assert (block.previous_block_hash == previous_block_hash)

            previous_block_hash = block.block_hash  # overwrite this for the next iteration
            
            assert Mining.verify_pow(block), "The PoW could not be verified!"
            Utils.log("Verified block hash (using nonce " + str(block.nonce) + ")")

            if validate_signatures:
                for transaction in block.transactions:
                    assert Utils.verify_signature(transaction.signature, transaction.pub_key,
                                                  transaction.unsigned_to_string)
                Utils.log("Verified transactions (" + str(len(block.transactions)) + ")")
            
            Utils.log("")

    def print_blockchain_data(self, print_transaction_data=True):
        """
        Print blockchain data to screen.
        """
        info = "BLOCKCHAIN DATA"
        print("=" * len(info))
        print("" + info)
        print("=" * len(info))
        print("CHAIN LENGTH : " + str(self.block_count))

        for block in self._blocks:
            
            info = "BLOCK " + str(block.height)
            print("\n" + info)
            print("=" * len(info))
            print("Block hash   : " + str(block.block_hash))
            print("Prev block   : " + str(block.previous_block_hash))
            print("Difficulty   : " + str(block.difficulty))
            print("Nonce        : " + str(block.nonce))
            print("Transactions : " + str(len(block.transactions)))

            if print_transaction_data:
                for i, transaction in enumerate(block.transactions):
                    tx_info = info + " - TRANSACTION " + str(i)
                    print("\n" + tx_info)
                    print("-" * len(tx_info))
                    transaction.print_transaction_data()
