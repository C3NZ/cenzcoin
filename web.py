from flask import Flask, jsonify
from flask_cors import CORS

from blockchain import Blockchain
from wallet import Wallet

# Setup server
app = Flask(__name__)
CORS(app)

# Setup wallet
wallet = Wallet()
blockchain = Blockchain(wallet.public_key)

@app.route('/', methods=['GET'])
def get_root():
    '''
        Test route
    '''
    return 'Initial setup!'

@app.route('/chain', methods=['GET'])
def get_chain():
    '''
        Get a snapshot of the current chain

        Status codes & Returns:
           :200: returns a snapshot of the chain in json 
    '''
    chain_snapshot = blockchain.chain
    dict_chain = [block.__dict__.copy() for block in chain_snapshot]
    for block in dict_chain:
        block['transactions'] = [transaction.__dict__ for transaction in block['transactions']]
    return (jsonify(dict_chain), 200)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
