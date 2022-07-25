import binascii
import base58
import base64
import ecdsa
import hashlib


class Utils:

    @staticmethod
    def log(message, debug_log=True):
        """Log a message"""
        if debug_log:
            print(message)

    @staticmethod
    def sha256(message):
        """Compute the double SHA256 hash of the message.

        :param message: (string) The message to compute the double SHA256 hash of.
        :return: The double SHA256 hash of the message.
        """
        assert isinstance(message, str), "message must be a string"

        hash1 = hashlib.sha256(message.encode("utf-8")).digest()
        return hashlib.sha256(hash1).hexdigest()

    @staticmethod
    def base58encode(pub_key_hash):
        """compute the base58 encoded public key from the public key hash"""
        checksum = Utils.sha256(pub_key_hash)[:4]  # create a checksum/fingerprint of the public key hash
        address = pub_key_hash + checksum  # concatenate the public key hash and its own checksum

        unencoded_string = binascii.unhexlify(address)
        return base58.b58encode(unencoded_string).decode("utf-8")

    @staticmethod
    def verify_signature(signature, pub_key, message):
        # Get signature in a format we can use to verify
        signature_b64_decoded_bytes = base64.b64decode(bytes(signature.encode('UTF-8')))
        
        if signature == "" or pub_key == "":
            raise Exception('No signature, public key combination provided!')
        
        # the public key(s) we get from the signed message:
        pubkeys = ecdsa.VerifyingKey.from_public_key_recovery(signature_b64_decoded_bytes, Utils.sha256(message).encode("UTF-8"), curve=ecdsa.SECP256k1)

        # the incoming public key was used to sign this message
        return pub_key in [pktmp.to_string().hex() for pktmp in pubkeys]
