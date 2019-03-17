from flask import Flask, jsonify
from flask_cors import CORS

from blockchain import Blockchain
from wallet import Wallet

# Setup server
app = Flask(__name__)
CORS(app)

# Setup wallet
app.wallet = Wallet()
app.blockchain = Blockchain(app.wallet.public_key)

@app.route('/', methods=['GET'])
def get_root():
    '''
        Test route
    '''
    return 'Initial setup!'

@app.route('/wallet', methods=['POST'])
def create_keys():
    '''
        Create a new pair of keys

    '''
    wallet = app.wallet

    wallet.create_keys()

    # 
    if wallet.save_keys():
        response = {
            'public_key': wallet.public_key,
            'private_key': wallet.private_key,
        }

        app.blockchain = Blockchain(wallet.public_key)
        return (jsonify(response), 201)

    # Keys weren't saved
    response = {
        'message': 'Saving the keys failed',
    }
    return (jsonify(response), 500)

@app.route('/wallet', methods=['GET'])
def load_keys():
    '''
        Load a pair of keys
    '''
    wallet = app.wallet

    if wallet.load_keys():
        response = {
            'public_key': wallet.public_key,
            'private_key': wallet.private_key,
        }
        app.blockchain = Blockchain(wallet.public_key)
        return (jsonify(response), 201)

    # Couldnt load the wallets 
    response = {
        'message': 'Couldnt load your private and public key',
    }
    return (jsonify(response), 500)

@app.route('/chain', methods=['GET'])
def get_chain():
    '''
        Get a snapshot of the current chain

        Status codes & Returns:
           :200: returns a snapshot of the chain in json 
    '''
    blockchain = app.blockchain
    chain_snapshot = blockchain.chain
    dict_chain = [block.__dict__.copy() for block in chain_snapshot]
    for block in dict_chain:
        block['transactions'] = [transaction.__dict__ for transaction in block['transactions']]
    return (jsonify(dict_chain), 200)

@app.route('/mine', methods=['POST'])
def mine():
    '''
        Mine a block on the blockchain
    '''
    # reference bc and wallet
    blockchain = app.blockchain
    wallet = app.wallet

    # mine a new block
    block = blockchain.mine_block()

    # Check if a block was returned
    if block:
        dict_block = block.__dict__.copy()
        dict_block['transactions'] = [transaction.__dict__ for transaction in dict_block['transactions']]

        response = {
            'message': 'A block was successfully added to the blockchain',
            'block': dict_block
        }
        return (jsonify(response), 201)

    # Mining the block was unsuccessful
    response = {
        'message': 'Adding a block failed',
        'wallet_set_up': not wallet.public_key
    }
    return (jsonify(response), 500)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
