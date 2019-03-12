'''
    Block module for blocks that are stored on the blockchain
'''
from time import time

class Block:
    '''
       Block class for representing a block within the blockchain 

        Properties:
            :index: the blocks index
            :previous_hash: the hash of the previous block
            :transactions: all transactions that occurred on this block
            :proof: the proof of work number used to create this block
            :timestamp: the time this block was created
    '''
    def __init__(self, index, previous_hash, transactions, proof, time=time()):
        self.index = index
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.proof = proof
        self.timestamp = time

    def __repr__(self):
        return (
            '''---BLOCK---\n'''
            f'''Index: {self.index}\n'''
            f'''Previous Hash: {self.previous_hash}\n'''
            f'''transactions: {self.transactions}\n'''
            f'''proof: {self.proof}'''
        )
