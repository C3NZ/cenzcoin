'''
    Node module - for any client related things to run the blockchainj
'''
from uuid import uuid4

from blockchain import Blockchain
from verification import Verification

class Node:

    def __init__(self):
        # self.id = str(uuid4())
        self.id = 'tempid'
        self.blockchain = Blockchain(self.id)

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
        else:
            print('-'*10)

    def listen_for_input(self):
        waiting_for_input = True
        bc = self.blockchain

        while waiting_for_input:
            print('Please choose')
            print('1: Add a new transaction value')
            print('2: Mine a new block')
            print('3: Output the blockchain blocks')
            print('4: Validate open transactions')
            print('q: quit')

            user_choice = self.get_user_choice()

            if user_choice == '1':
                recipient, amount = self.get_transaction_value()
                if bc.add_transaction(self.id, recipient, amount):
                    print('Added transaction!')
                else:
                    print('Transaction failed')
            elif user_choice == '2':
                bc.mine_block()
            elif user_choice == '3':
                self.print_blockchain_elements()
            elif user_choice == '4':
                if Verification.verify_transactions(bc.open_transactions, bc.get_balance):
                    print('all open transactions are currently valid')
                else:
                    print('There are invalid transactions')
            elif user_choice == 'q':
                waiting_for_input = False

            # Use a format string to create a formatted string indicating who the owner is and what their balance is 
            print(f'Balance of {self.id}: {bc.get_balance():6.2f}')

            # Verify the blockchain over every action
            if not Verification.verify_chain(bc):
                self.print_blockchain_elements()
                print('Invalid blockchain!')
                break
        print('Blockchain now shutting down')


if __name__ == '__main__':
    node = Node()
    node.listen_for_input()
