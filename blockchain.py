# std lib imports
import json
import pickle
import pdb
import sys
from collections import OrderedDict
from functools import reduce

# Own imports
from hash_util import hash_string_256, hash_block
from files import save_data, load_data
from block import Block
from transaction import Transaction
from verification import Verification

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
    '''
    def __init__(self, hosting_node_id):
        self.chain, self.open_transactions = load_data(from_json=True)
        self.verifier = Verification() 
        self.hosting_node = hosting_node_id

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

        while not self.verifier.valid_proof(self.open_transactions, last_hash, proof):
            proof += 1

        return proof


    def get_balance(self):
        '''
            Gets the total balance of a single participants

            Arguments:
                :participant: the name of the participant that we want the balance of

            Returns:
                The balance of the participant
        '''
        participant = self.hosting_node

        # Get the total transactions where the participant is the sender (both open and closed)
        tx_sent = [[tx.amount for tx in block.transactions if tx.sender == participant] for block in self.chain]
        open_tx_sent = [[tx.amount for tx in self.open_transactions if tx.sender == participant]]
        tx_sent.extend(open_tx_sent)

        # Sum up the amount the participant has sent
        amount_sent = reduce(sum_transactions, tx_sent, 0)

        # Get the total transactions where the participant is the receiver (strictly closed)
        tx_received = [[tx.amount for tx in block.transactions if tx.recipient == participant] for block in self.chain]

        # Sum up the amount the participant has received
        amount_received = reduce(sum_transactions, tx_received, 0)

        # Return the users balance
        return amount_received - amount_sent

    def get_last_blockchain_value(self):
        '''
            Grab the last block from the blockchain

            Returns:
                The last block on the blockchain
        '''
        if len(self.chain) < 1:
            return None
        else:
            return self.chain[-1]


    def add_transaction(self, sender, recipient, amount=1.0):
        '''
            Append a new value as well as the last blockcahin value to the block chain

            Arguments:
                    :sender: The sender of the coins
                    :recipient: The recipient of the coins.
                    :amount: The amount of coins sent with the transaction(default=1.0)

            Returns:
                True if the transaction is valid, False otherwise
        '''


        # Use an ordered dict to always ensure the order of keys inside of the dictionary (for consistent hashing)
        # dicts return keys that arent in any specific order, which when stringified, can ruin a hash value. An ordered
        # dict orders the key that are entered the order that they're entered in, allowing us to have consistent hashing
        transaction = Transaction(sender, recipient, amount)
        # If the transaction is legitimate, add it to the open transactions list and
        # keep track of participants
        if self.verifier.verify_transaction(transaction, self.get_balance):
            self.open_transactions.append(transaction)
            return True

        return False

    def mine_block(self):
        '''
            Mine the current block on the blockchain

            Returns:
                True if successful
        '''
        last_block = self.chain[-1]
        hashed_block = hash_block(last_block)
        proof = self.proof_of_work()

        reward_tx = Transaction('MINING', self.hosting_node, MINING_REWARD)

        # Modify a local list of transactions so that users don't get rewarded if 
        # mining turns out to be unsuccessful
        copied_transactions = self.open_transactions[:]
        copied_transactions.append(reward_tx)

        # Create the k,v pairs inside of tuples for the ordered dictionary to insert them in the order
        # we specify the list
        index = len(self.chain)
        previous_hash = hashed_block
        transactions = copied_transactions

        # Create our block, append it to the blockchain, and then save the blockchain
        block = Block(index, previous_hash, transactions, proof)
        self.chain.append(block)
        save_data(self.chain, self.open_transactions, to_json=True)
        self.open_transactions = []
        return True


if __name__ == '__main__':
    # add debug to the command to enter debug mode
    if len(sys.argv) >= 2 and sys.argv[1] == 'debug':
        pdb.set_trace()
    main()
