from mockchain.utils import Utils
from mockchain.block import Block


class Mining:

    @staticmethod
    def generate_block(mempool_transactions, previous_block, difficulty):
        """

        TODO If implementing UTXO and block reward logic, sort by fees and pay the fee to your miner node
        """
        block = Block()

        # Pick transactions from the mempool to this block
        # In Bitcoin, this picking would sort by fees that would go to the miner
        for transaction in mempool_transactions.get_transactions:
            block.append_transaction(transaction)

        # now clean up the mempool because we added the transactions to this block
        for transaction in block.transactions:
            mempool_transactions.remove_transaction(transaction)
        
        block.previous_block_hash = previous_block.block_hash
        block.height = previous_block.height + 1

        Mining.mine(block, difficulty)

        # we mined a block; report it:
        Utils.log('\nFound block ' + str(block.height) + ' using nonce ' + str(block.nonce))
        Utils.log('  Block ' + str(block.height) + ' hash: ' + block.block_hash + '\n')

        block.print_transaction_ids()  # report the transactions included in the block

        return block

    @staticmethod
    def verify_pow(block=None):
        """Verify Proof-of-Work"""
        assert block.difficulty >= 1, "Please specify a block difficulty >= 1"

        digest = block.block_hash
        prefix = "0" * block.difficulty

        return digest.startswith(prefix)

    @staticmethod
    def mine(block, difficulty=1):
        """
        # TODO Implement difficulty as hexadecimal base/exponent calculation
        """
        assert difficulty >= 1, "Please specify a block difficulty >= 1"
        block.difficulty = difficulty

        i = 0
        while True:
            block.nonce = i
            block.recompute_block_hash()  # produce a new hash based on the changed nonce

            if Mining.verify_pow(block):
                # we solved it!
                break
            
            i += 1
