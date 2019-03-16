from flask import Flask
from flask_cors import CORS

from wallet import Wallet

# Setup server
app = Flask(__name__)
CORS(app)

# Setup wallet
wallet = Wallet()

@app.route('/', methods=['GET'])
def get_root():
    return 'Initial setup!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
