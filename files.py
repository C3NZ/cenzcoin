'''
    Blockchain file module
'''

# std lib imports
import json
import pickle
from collections import OrderedDict

# Own imports
from block import Block

def save_data(blockchain, open_transactions, to_json=False):
    '''
        Save the blockchain to a file
    '''
    mode = 'wb'
    filename = 'blockchain.p'

    if to_json:
        mode = 'w'
        filename = 'blockchain.txt'

    try:
        with open(filename, mode) as open_file:

            # Write the blockchain to file as either text or binary
            if to_json:
                saveable_chain = [block.__dict__ for block in blockchain]
                open_file.write(json.dumps(saveable_chain))
                open_file.write('\n')
                open_file.write(json.dumps(open_transactions))
            else:
                binary_data = {
                    'blockchain': blockchain,
                    'ot': open_transactions
                }

                open_file.write(pickle.dumps(binary_data))
    except IOError:
        print('File couldnt be saved')

def parse_json_block(block):
    '''
        parse a json version of a block on the blockchain

        Arguments:
            :block: the block being parsed

        Returns:
            the parsed blocked to be added to the blockchain
    '''

    index = block['index']
    previous_hash = block['previous_hash']
    transactions = []
    proof = block['proof']
    timestamp = block['timestamp']

    # Get all transactions from the block
    for curr_tx in block['transactions']:
        # Bundle the data for the transaction
        tx_data = [
            ('sender', curr_tx['sender']),
            ('recipient', curr_tx['recipient']),
            ('amount', curr_tx['amount'])
        ]

        # create the current transaction as an ordered dict (for hashing consistency)
        curr_tx = OrderedDict(tx_data)
        transactions.append(curr_tx)

    # Create the new block
    parsed_block = Block(index, previous_hash, transactions, proof, timestamp)
    return parsed_block

def parse_json_ot(open_tx):
    '''
        parse a json transaction

        Arguments:
            :json_ot: the json version of the open transaction
    '''
    tx_data = [
        ('sender', open_tx['sender']),
        ('recipient', open_tx['recipient']),
        ('amount', open_tx['amount'])
    ]

    # Create the outstanding transaction and return it  
    ot_tx = OrderedDict(tx_data)
    return ot_tx

def load_data(from_json=False):
    '''
        Load the blockchain from a file 
    '''
    mode = 'rb'
    filename = 'blockchain.p'

    if from_json:
        mode = 'r'
        filename = 'blockchain.txt'

    blockchain = []
    open_transactions = []

    try:
        # Open either the json or binary file
        with open(filename, mode) as open_file:
            # Handle either json or pickle file
            if from_json:
                # grab the lines, the blockchain from them, and then create the real blockchain 
                lines = open_file.readlines()
                json_chain = json.loads(lines[0][:-1])
                blockchain = []

                # Iterate over every block and parse them all from json
                for block in json_chain:
                    real_block = parse_json_block(block)
                    blockchain.append(real_block)

                # Load the open transactions from the json and create the open transactions list
                json_ot = json.loads(lines[1])
                open_transactions = []

                # Iterate over the open transactions, parse them, and then add them to the open transactions list 
                for json_tx in json_ot:
                    tx_dict = parse_json_ot(json_tx)
                    open_transactions.append(tx_dict)
            else:
                # Load the blockchain from a pickle file
                saved_data = pickle.loads(open_file.read())
                blockchain = saved_data['blockchain']
                open_transactions = saved_data['ot']
    except (IOError, IndexError):
        # handle an IO error ocurring
        print('File couldnt be loaded, creating a new blockchain')

        # Create genesis block information
        index = 0
        previous_hash = 'genesis'
        transactions = []
        proof = 100
        timestamp = 0

        # Create the new blockchain and open_transactions
        genesis_block = Block(index, previous_hash, transactions, proof, timestamp)
        blockchain = [genesis_block]
        open_transactions = []
    finally:
        # Load blockchain and return it to client
        print("Blockchain and open transactions loaded")
        return (blockchain, open_transactions)
