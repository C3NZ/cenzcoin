'''
    Verification module - for handling blockchain related verification
'''

from hash_util import hash_string_256, hash_block

class Verification:
    '''
        Module for Blockchain verification handling 
    '''
    @staticmethod
    def valid_proof(transactions, last_hash, proof):
        '''
            Check to see if the current proof is valid

            Arguments:
                :transactions: the list of transactions on the block
                :last_hash: the hash of the previous block
                :proof: the proof number used for attempting to generate a valid hash

            Returns:
                True if the guessed hash has two leading 0s, False otherwise
        '''
        hashable_txs = [tx.to_ordered_dict() for tx in transactions]
        guess = (str(hashable_txs) + str(last_hash) + str(proof)).encode()
        guessed_hash = hash_string_256(guess)

        return guessed_hash[:2] == '00'

    @classmethod
    def verify_chain(cls, blockchain):
        '''
            Verify the current blockchain

            Returns:
                True if the blockchain is valid, False otherwise
        '''

        # Enumerate the blockchain in order to retrieve the current block & it's index
        for index, block in enumerate(blockchain.chain):
            if index == 0:
                continue

            # Ensure the current blocks previous hash matches the hash of the previous block
            if block.previous_hash != hash_block(blockchain.chain[index - 1]):
                print('The previous hash doesnt match the hash of the block on the blockchain ')
                return False

            #Select every part of the list except for the last element 
            # in the transactions (the reward transaction) because it is not part of the proof of work calculation
            if not cls.valid_proof(block.transactions[:-1], block.previous_hash, block.proof):
                print('Proof of work is invalid')
                return False

        return True

    @staticmethod
    def verify_transaction(transaction, get_balance):
        '''
            Veryify that the participant has a high enough balance in order to complete
            a transaction

            Arguments:
                :transacation: The transaction that we're trying to verify
                :get_balance: A reference to a function that can calculate the balance of a bc participant

            Returns:
                True if the sender balance is greater than the tx amount and that
                the tx amount is greater than 0
        '''
        sender_balance = get_balance()

        return sender_balance >= transaction.amount and transaction.amount > 0

    @classmethod
    def verify_transactions(cls, open_transactions, get_balance):
        '''
            Validate that all open transactions within the open transactions

            Arguments:
                :open_transactions: a list of open transaction objects
                :get_balance: A reference to a function that can calculate the balance of a bc participant

            Returns:
                True if all transactions are valid, False otherwise.
        '''
        return all(cls.verify_transaction(tx, get_balance) for tx in open_transactions)

