from Crypto.PublicKey import RSA
from Crypto import Random 
import binascii


class Wallet:
    def __init__(self):
        self.private_key = None
        self.public_key = None

    def create_keys(self):
        self.private_key, self.public_key = self.generate_keys()

    def generate_keys(self):
        # Generate a 1024 bit rsa key object using Crypto.Random 
        # for a more secure random int generation algorithim
        rsa_obj = RSA.generate(1024, Random.new().read)

        # Grab the private key as a binary encoded byte string
        private_key = rsa_obj.exportKey(format="DER")

        # Derive public key information and then export it as a binary encoded byte string
        public_key = rsa_obj.publickey().exportKey(format="DER")

        # Convert binary encoded byte strings into hex and then decode the hex into ascii characters.
        private_key_string = binascii.hexlify(private_key).decode('ascii')
        public_key_string = binascii.hexlify(public_key).decode('ascii')

        return (private_key_string, public_key_string)
