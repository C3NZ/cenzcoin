'''
    Block module for blocks that are stored on the blockchain
'''
from time import time

class Block:
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
