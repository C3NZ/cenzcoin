'''
    Blockchain module - for all functionality related to the blockchain itself
'''
# std lib imports
from functools import reduce

# Own imports
from util.hash_util import hash_block
from util.files import save_data, load_data
from util.verification import Verification
from block import Block
from transaction import Transaction

from wallet import Wallet

MINING_REWARD = 10

def sum_transactions(tx_sum, txs):
    '''
        get_balance helper function for summing a users transaction total

        Arguments:
            tx_sum: the total sum of all the current transactions
            txs: all transactions from the currently evaluated block
    '''
    # Check if there are any transactions on the current checked block
    if txs:
        return tx_sum + sum(txs)

    return tx_sum


class Blockchain:
    '''
        Blockchain class

        Properties:
            :chain: the blockchain itself (list of blocks)
            :open_transactions: all open transactions
            :hosting_node: the node currently hosting this blockchain
    '''
    def __init__(self, hosting_node_id):
        self.__chain, self.__open_transactions = load_data(from_json=True)
        self.hosting_node = hosting_node_id

    @property
    def chain(self):
        '''
            Return a copied version of the blockchain
        '''
        return self.__chain[:]

    @chain.setter
    def chain(self, value):
        self.__chain = value

    @property
    def open_transactions(self):
        '''
            Get a copy of the open transactions attached to the blockchain
        '''
        return self.__open_transactions[:]

    @open_transactions.setter
    def open_transactions(self, value):
        self.__open_transactions = value

    def proof_of_work(self):
        '''
            Calculate a valid proof of work

            Returns:
                proof number that generates a valid hash
        '''
        # The last block added to the blockchain
        last_block = self.chain[-1]
        last_hash = hash_block(last_block)
        proof = 0

        while not Verification.valid_proof(self.__open_transactions, last_hash, proof):
            proof += 1

        return proof

    def get_amount_sent(self, participant):
        '''
            Get the amount of coins sent by a participant (open and closed)

            Parameters:
                :participant: the participant you're trying to get the balance of

            Returns:
                The amount the participant has sent
        '''
        # Get the total transactions where the participant is the sender (both open and closed)
        tx_sent = [[tx.amount for tx in block.transactions if tx.sender == participant] for block in self.__chain]
        open_tx_sent = [[tx.amount for tx in self.__open_transactions if tx.sender == participant]]
        tx_sent.extend(open_tx_sent)

        # Sum up the amount the participant has sent
        amount_sent = reduce(sum_transactions, tx_sent, 0)

        return amount_sent

    def get_amount_received(self, participant):
        '''
            Get the total amount received by the participant

            Parameters:
                :participant: the participant you're trying to find the total amt of coins received

            Returns:
                The amount the participant has received
        '''
        # Get the total transactions where the participant is the receiver (strictly closed)
        tx_received = [[tx.amount for tx in block.transactions if tx.recipient == participant] for block in self.__chain]

        # Sum up the amount the participant has received
        amount_received = reduce(sum_transactions, tx_received, 0)

        return amount_received

    def get_balance(self):
        '''
            Gets the total balance of a single participant

            Returns:
                The balance of the participant
        '''
        participant = self.hosting_node

        # Get both the amount sent and received by the participant
        amount_sent = self.get_amount_sent(participant)
        amount_received = self.get_amount_received(participant)

        # Return the users balance
        return amount_received - amount_sent

    def get_last_blockchain_value(self):
        '''
            Grab the last block from the blockchain

            Returns:
                The last block on the blockchain
        '''
        if self.__chain:
            return None
        else:
            return self.__chain[-1]


    def add_transaction(self, sender, recipient, signature, amount=1.0):
        '''
            Append a new value as well as the last blockcahin value to the block chain

            Arguments:
                    :sender: The sender of the coins
                    :recipient: The recipient of the coins.
                    :amount: The amount of coins sent with the transaction(default=1.0)

            Returns:
                True if the transaction is valid, False otherwise
        '''

        #Transaction failed, the wallet isn't setup.
        if not self.hosting_node:
            return False

        # Use an ordered dict to always ensure the order of keys inside of the dictionary (for consistent hashing)
        # dicts return keys that arent in any specific order, which when stringified, can ruin a hash value. An ordered
        # dict orders the key that are entered the order that they're entered in, allowing us to have consistent hashing
        transaction = Transaction(sender, recipient, signature, amount)

        # If the transaction is legitimate, add it to the open transactions list and
        # keep track of participants
        if Verification.verify_transaction(transaction, self.get_balance):
            self.__open_transactions.append(transaction)
            save_data(self.__chain, self.__open_transactions, to_json=True)
            return True

        return False

    def mine_block(self):
        '''
            Mine the current block on the blockchain

            Returns:
                True if successful
        '''
        #Mine failed, the wallet isn't setup.
        if not self.hosting_node:
            return False

        last_block = self.__chain[-1]
        hashed_block = hash_block(last_block)
        proof = self.proof_of_work()

        # Modify a local list of transactions so that users don't get rewarded if 
        # mining turns out to be unsuccessful
        copied_transactions = self.__open_transactions[:]

        # Verify all copied transactions
        for transaction in copied_transactions:
            if not Wallet.verify_transaction(transaction):
                self.__open_transactions.remove(transaction)
                return False

        # Create the reward transaction and add it to the copied transactions list
        reward_tx = Transaction('MINING', self.hosting_node, '', MINING_REWARD)
        copied_transactions.append(reward_tx)

        # Create the k,v pairs inside of tuples for the ordered dictionary to insert them in the order
        # we specify the list
        index = len(self.__chain)
        previous_hash = hashed_block
        transactions = copied_transactions

        # Create our block, append it to the blockchain, and then save the blockchain
        block = Block(index, previous_hash, transactions, proof)

        self.__chain.append(block)
        self.__open_transactions = []
        save_data(self.__chain, self.__open_transactions, to_json=True)
        return True
