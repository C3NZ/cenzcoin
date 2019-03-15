'''
    Node module - for any client related things to run the blockchain
'''

# Own imports
from blockchain import Blockchain
from util.verification import Verification
from wallet import Wallet

class Node:
    '''
        The blockchain node interface class

        Attributes:
            :wallet: the current nodes wallet
            :blockchain: The current blockchain that is connected to the node
    '''
    def __init__(self):
        self.wallet = Wallet()
        self.blockchain = None

    def get_transaction_value(self):
        '''
            Get the transaction recipient and value 

            Returns:
                :recipient: tx recipient as a string
                :amount: tx amount as a float
        '''
        recipient = input('Enter the recipient of the transaction: ')
        amount = float(input('Your transaction amount please: '))
        return recipient, amount

    def get_user_choice(self):
        '''
            Prompts the user for its choice and return it.

            Returns:
                :user_input: the users input as a string
        '''
        user_input = input('Your choice: ')
        return user_input

    def print_blockchain_elements(self):
        '''
            Output all blocks of the blockchain
        '''
        for block in self.blockchain.chain:
            print(block)

        print('-'*10)

    def listen_for_input(self):
        '''
            Listen for user input
        '''
        waiting_for_input = True
        b_chain = self.blockchain

        while waiting_for_input:
            # Make sure that we're always using the current blockchain

            print('Please choose')
            print('1: Add a new transaction value')
            print('2: Mine a new block')
            print('3: Output the blockchain blocks')
            print('4: Validate open transactions')
            print('5: Create wallet')
            print('6: Save wallet')
            print('7: Load wallet')
            print('q: quit')

            user_choice = self.get_user_choice()

            if user_choice == '1':
                recipient, amount = self.get_transaction_value()
                signature = self.wallet.sign_transaction(self.wallet.public_key, recipient, amount)
                if b_chain.add_transaction(self.wallet.public_key, recipient, signature, amount):
                    print('Added transaction!')
                else:
                    print('Transaction failed')
            elif user_choice == '2':
                if not b_chain.mine_block():
                    print('Mining failed. Is your wallet configured?')
            elif user_choice == '3':
                self.print_blockchain_elements()
            elif user_choice == '4':
                if Verification.verify_transactions(b_chain.open_transactions, b_chain.get_balance):
                    print('all open transactions are currently valid')
                else:
                    print('There are invalid transactions')
            elif user_choice == '5':
                self.wallet.create_keys()
                b_chain = self.blockchain = Blockchain(self.wallet.public_key)
            elif user_choice == '6':
                self.wallet.save_keys()
            elif user_choice == '7':
                self.wallet.load_keys()
                b_chain = self.blockchain = Blockchain(self.wallet.public_key)
            elif user_choice == 'q':
                waiting_for_input = False

            # Use a format string to create a formatted string indicating
            # who the owner is and what their balance is
            print(f'Balance of {self.wallet.public_key}: {b_chain.get_balance():6.2f}')

            # Verify the blockchain over every action
            if not Verification.verify_chain(b_chain):
                self.print_blockchain_elements()
                print('Invalid blockchain!')
                break
        print('Blockchain now shutting down')


def main():
    '''
        Run a new node instance
    '''
    node = Node()
    node.listen_for_input()

if __name__ == '__main__':
    main()
