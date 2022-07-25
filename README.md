How to run:

Go to the root of the project (where src/ is located).
Then run with python, e.g. (depends on your python setup):

    python main.py

The code is in the src/ folder.

---
Description:

In src/ you will find a skeleton structure of a very basic blockchain

Your task is to implement all the missing logic in all the TODO sections of the code

This includes: Private and public key generation sha256 and ripemd160 hashes for hashing public keys, blocks and transactions base58 address encoding from a PKH Signatures and signature verification

Mining logic: Creating block hashes from relevant data Proof of Work logic for finding a block with correct difficulty

Adding and removing transactions from mempool

Proof of Work and block/signature verification

BONUS things to implement:
Implement UTXO logic so that each TX is dependant on a previous TX Each TX is locked to a pubkey hash so that only a corresponding pubkey can spend the TX by satisfying the locking script You will need to also implement the locking and unlocking script logic from Week 2 Implement the concept of Coinbase transactions (block reward = block subsidy + fees)

Block generation: If implementing UTXO and block reward logic, sort by fees and pay the fee to your miner node Implement difficulty as hexadecimal base/exponent calculation The blockchain skeleton code is taken from a public github project which will be disclosed later
