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

# Mining reward for users mining blocks
MINING_REWARD = 10

# Initialize some other global variables
open_transactions = []
owner = 'cenz'

# Load the block (From either json or binary )
blockchain, open_transactions = load_data(from_json=True)

verifier = Verification()

def proof_of_work():
    '''
        Calculate a valid proof of work

        Returns:
            proof number that generates a valid hash
    '''
    # The last block added to the blockchain
    last_block = blockchain[-1]
    last_hash = hash_block(last_block)
    proof = 0

    while not verifier.valid_proof(open_transactions, last_hash, proof):
        proof += 1

    return proof


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

def get_balance(participant):
    '''
        Gets the total balance of a single participants

        Arguments:
            :participant: the name of the participant that we want the balance of

        Returns:
            The balance of the participant
    '''

    # Get the total transactions where the participant is the sender (both open and closed)
    tx_sent = [[tx.amount for tx in block.transactions if tx.sender == participant] for block in blockchain]
    open_tx_sent = [[tx.amount for tx in open_transactions if tx.sender == participant]]
    tx_sent.extend(open_tx_sent)

    # Sum up the amount the participant has sent
    amount_sent = reduce(sum_transactions, tx_sent, 0)

    # Get the total transactions where the participant is the receiver (strictly closed)
    tx_received = [[tx.amount for tx in block.transactions if tx.recipient == participant] for block in blockchain]

    # Sum up the amount the participant has received
    amount_received = reduce(sum_transactions, tx_received, 0)

    # Return the users balance
    return amount_received - amount_sent

def get_last_blockchain_value():
    '''
        Grab the last block from the blockchain

        Returns:
            The last block on the blockchain
    '''
    if len(blockchain) < 1:
        return None
    else:
        return blockchain[-1]


def add_transaction(sender, recipient, amount=1.0):
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
    if verifier.verify_transaction(transaction, get_balance):
        open_transactions.append(transaction)
        return True

    return False

def mine_block():
    '''
        Mine the current block on the blockchain

        Returns:
            True if successful
    '''
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)
    proof = proof_of_work()

    reward_tx = Transaction('MINING', owner, MINING_REWARD)

    # Modify a local list of transactions so that users don't get rewarded if 
    # mining turns out to be unsuccessful
    copied_transactions = open_transactions[:]
    copied_transactions.append(reward_tx)

    # Create the k,v pairs inside of tuples for the ordered dictionary to insert them in the order
    # we specify the list
    index = len(blockchain)
    previous_hash = hashed_block
    transactions = copied_transactions

    # Create our block, append it to the blockchain, and then save the blockchain
    block = Block(index, previous_hash, transactions, proof)
    blockchain.append(block)
    save_data(blockchain, open_transactions, to_json=True)
    return True


def get_transaction_value():
    '''
        Get the transaction recipient and value 

        Returns:
            :recipient: tx recipient as a string
            :amount: tx amount as a float
    '''
    recipient = input('Enter the recipient of the transaction: ')
    amount = float(input('Your transaction amount please: '))
    return recipient, amount

def get_user_choice():
    '''
        Prompts the user for its choice and return it.

        Returns:
            :user_input: the users input as a string
    '''
    user_input = input('Your choice: ')
    return user_input

def print_blockchain_elements():
    '''
        Output all blocks of the blockchain
    '''
    for block in blockchain:
        print('Outputting Block')
        print(block)
    else:
        print('-' * 20)

def main():
    '''
        Entry function for the blockchain to operate
    '''
    waiting_for_input = True
    global open_transactions

    while waiting_for_input:
        print('Please choose')
        print('1: Add a new transaction value')
        print('2: Mine a new block')
        print('3: Output the blockchain blocks')
        print('4: Validate open transactions')
        print('q: quit')

        user_choice = get_user_choice()

        if user_choice == '1':
            recipient, amount = get_transaction_value()
            if add_transaction(owner, recipient, amount):
                print('Added transaction!')
            else:
                print('Transaction failed')
        elif user_choice == '2':
            if mine_block():
                open_transactions = []
        elif user_choice == '3':
            print_blockchain_elements()
        elif user_choice == '4':
            if verifier.verify_transactions(open_transactions, get_balance):
                print('all open transactions are currently valid')
            else:
                print('There are invalid transactions')
        elif user_choice == 'q':
            waiting_for_input = False

        # Use a format string to create a formatted string indicating who the owner is and what their balance is 
        print(f'Balance of {owner}: {get_balance(owner):6.2f}')

        # Verify the blockchain over every action
        if not verifier.verify_chain(blockchain):
            print_blockchain_elements()
            print('Invalid blockchain!')
            break
    print('Blockchain now shutting down')

if __name__ == '__main__':
    # add debug to the command to enter debug mode
    if len(sys.argv) >= 2 and sys.argv[1] == 'debug':
        pdb.set_trace()
    main()
