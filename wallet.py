'''
    Wallet module - for creating instances of user wallets to engage in transactions 
                    on the blockchain
'''
# std lib imports
import binascii

# installed package imports
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from Crypto import Random

# own imports
from util.files import save_keys, load_keys

class Wallet:
    '''
        The implementation of a users wallet

        Attributes:
            :private_key: the key used for identifying the owner of the wallet
                          and signing transactions. This should be kept PRIVATE.
            :public_key:  the key used for verifying that transactions initiated by this account
                          are legimimate.
    '''
    def __init__(self):
        self.private_key = None
        self.public_key = None

    def create_keys(self):
        '''
            Generate a new pair of keys for the user
        '''
        self.private_key, self.public_key = self.generate_keys()

    def save_keys(self):
        '''
            Save the wallets private and public keys
        '''

        # Make sure there are keys to save 
        if self.private_key and self.public_key:
            save_keys(self.private_key, self.public_key)
        else:
            print('You need both a private and public key to save it to a file')

    def load_keys(self):
        '''
            Attempt to load a pair of keys from the users wallet
        '''
        self.private_key, self.public_key = load_keys()

        if not self.private_key or not self.public_key:
            print('Creating a new pair of keys')
            self.create_keys()

    def generate_keys(self):
        '''
            Generate a new pair of 1024 bit RSA keys.
        '''
        # Generate a 1024 bit rsa key object using Crypto.Random 
        # for a more secure random int generation algorithim
        rsa_obj = RSA.generate(1024, Random.new().read)

        # Grab the private key as a binary encoded byte string
        private_key = rsa_obj.exportKey(format="DER")

        # Derive public key information and then export it as a binary encoded byte string
        public_key = rsa_obj.publickey().exportKey(format="DER")

        # Convert binary encoded byte strings into hex and then decode the hex into ascii characters
        private_key_string = binascii.hexlify(private_key).decode('ascii')
        public_key_string = binascii.hexlify(public_key).decode('ascii')

        return (private_key_string, public_key_string)

    def sign_transaction(self, sender, recipient, amount):
        '''
            Sign transactions that are authorized with this wallet for good security measures

            Parameters:
                :sender: (Yourself in this instance)
                :recipient: The recipients wallet
                :amount: the amount being sent to the recipient
        '''
        # Convert the users private key back into a binary encoded byte string
        binary_key = binascii.unhexlify(self.private_key)

        # With the users private key, create a new object named signer to authenticate
        # a message with their private key
        signer = PKCS1_v1_5.new(RSA.importKey(binary_key))

        # create a sha256 hash of the current transaction as the payload to be signed
        payload = SHA256.new((str(sender) + str(recipient) + str(amount)).encode('utf8'))

        # Sign the payload as proof that this transaction was initiated by th
        binary_signature = signer.sign(payload)

        # Convert the binary encoded signature back into ascii
        str_signature = binascii.hexlify(binary_signature).decode('ascii')

        return str_signature

    @staticmethod
    def verify_transaction(transaction):
        '''
            Verify a transaction from a user
        '''
        if transaction.sender == 'MINING':
            return True

        # Convert the public key into a binary encoded byte string and then 
        # create an RSA public key object from it
        binary_key = binascii.unhexlify(transaction.sender)
        public_key = RSA.importKey(binary_key)

        # Create a new verifier object from the senders public key
        verifier = PKCS1_v1_5.new(public_key)

        # Hash the transaction to obtain a payload
        payload = SHA256.new((transaction.sender + transaction.recipient + str(transaction.amount)).encode('utf8'))

        # Grab a binary version of the users signature
        binary_signature = binascii.unhexlify(transaction.signature)

        # Confirm whether or not the signature generated from the senders public key matches the
        # signature attached to the transaction
        return verifier.verify(payload, binary_signature)
