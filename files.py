'''
    Blockchain file module
'''
import json
import pickle

from collections import OrderedDict

def save_data(blockchain, open_transactions, to_json=False):
    '''
        Save the blockchain to a file
    '''
    mode = 'wb'
    if to_json:
        mode = 'w'

    with open('blockchain.p', mode) as open_file:

        # Write the blockchain to file as either text or binary
        if to_json:
            open_file.write(json.dumps(blockchain))
            open_file.write('\n')
            open_file.write(json.dumps(open_transactions))
        else:
            binary_data = {
                'blockchain': blockchain,
                'ot': open_transactions
            }

            open_file.write(pickle.dumps(binary_data))

def parse_json_block(block):
    '''
        parse a json version of a block on the blockchain

        Arguments:
            :block: the block being parsed

        Returns:
            the parsed blocked to be added to the blockchain
    '''
    # Get all transactions from the block
    all_tx = []
    for curr_tx in block['transactions']:
        # Bundle the data for the transaction
        tx_data = [
            ('sender', curr_tx['sender']),
            ('recipient', curr_tx['recipient']),
            ('amount', curr_tx['amount'])
        ]

        # create the current transaction as an ordered dict (for hashing consistency)
        curr_tx = OrderedDict(tx_data)
        all_tx.append(curr_tx)

    # Bundle the data for the block
    parsed_block_data = [
        ('previous_hash', block['previous_hash']),
        ('index', block['index']),
        ('transactions', all_tx),
        ('proof', block['proof'])
    ]

    # Create the parsed block and then return it
    parsed_block = OrderedDict(parsed_block_data)
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
    if from_json:
        mode = 'r'

    blockchain = []
    open_transactions = []

    # Open either the json or binary file
    with open('blockchain.p', mode) as open_file:
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


        return (blockchain, open_transactions)

