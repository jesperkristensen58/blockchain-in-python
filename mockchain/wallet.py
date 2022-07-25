import base64
import binascii
import hashlib
from mockchain.utils import Utils
import ecdsa

__all__ = ["Wallet"]


class Wallet:
    """
    Represent a Wallet.

    The wallet can sign a transaction.
    """

    def __init__(self):

        # the "signing key" is the private key:
        signing_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
        private_key = signing_key.to_string().hex()  # represent as HEX
        
        vk = signing_key.get_verifying_key()  # the "verifying key" is the public key
        public_key = vk.to_string().hex()

        # the pub key hash is just = RIPEMD160(SHA256(public_key))
        public_key_bytes = binascii.unhexlify(public_key)  # convert public key in hex to bytes via "unhexlify"
        tmp_sha256 = hashlib.new('sha256', public_key_bytes).digest()
        pub_key_hash = hashlib.new('ripemd160', tmp_sha256).hexdigest()  # the result is 20 bytes and in hex

        # store the values
        self._private_key = private_key
        self._public_key = public_key
        self.pub_key_hash = pub_key_hash

    @property
    def identity(self):
        return self.pub_key_hash

    def sign_transaction(self, transaction):
        if transaction.sender != self.identity:
            raise Exception('The sender must be the one signing the transaction')
        
        # Create our text to sign
        message = transaction.unsigned_to_string

        digest = Utils.sha256(message).encode("utf-8")
        sk = ecdsa.SigningKey.from_string(binascii.unhexlify(self._private_key), curve=ecdsa.SECP256k1)
        signature = sk.sign(digest)

        # Get signature as b64 encoded string
        signature_b64_encoded = base64.b64encode(signature).decode('utf-8')

        # update the transaction with the signature and the signer
        transaction.signature = signature_b64_encoded
        transaction.pub_key = self._public_key
