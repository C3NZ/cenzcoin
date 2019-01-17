import sys

# Initialize our (empty) blockchain list
blockchain = []
open_transactions = []
owner = 'cenz'

def get_last_blockchain_value():
    '''
        Returns the last value of the current blockchain.
    '''
    if len(blockchain) < 1:
        return None
    else:
        return blockchain[-1]

def add_transaction(sender, recipient, amount=1.0):
    '''
        Append a new value as well as the last blockcahin value to the block chain

        Arguments:
                :sender: The sender of the coins
                :recipient: The recipient of the coins.
                :amount: The amount of coins sent with the transaction(default=1.0)
    '''

    transaction = {'sender': sender, 'recipient': recipient, 'amount': amount}
    open_transactions.append(transaction)

def mine_block():
    pass

def get_transaction_value():
    '''
        Returns the recipient and amount being sent to the recipient in a tuple
    '''
    recipient = input('Enter the recipient of the transaction: ')
    amount = float(input('Your transaction amount please: '))
    return recipient, amount

def get_user_choice():
    '''
        Prompts the user for its choice and return it.
    '''
    user_input = input('Your choice: ')
    return user_input

def print_blockchain_elements():
    '''
        Output all blocks of the blockchain 
    '''
    for block in blockchain:
        print('Outputting Block')
        print(block)
    else:
        print('-' * 20)

def verify_chain():
    '''
        verify the current blockchain and return True if its valid. False otherwise
    '''

    is_valid = True

    for block_index in range(len(blockchain)):
        if block_index == 0:
            continue
        elif blockchain[block_index][0] == blockchain[block_index - 1]:
            is_valid = True
        else:
            is_valid = False

def main():
    waiting_for_input = True

    while waiting_for_input:
        print('Please choose')
        print('1: Add a new transaction value')
        print('2: Output the blockchain blocks')
        print('h: Manipulate the chain')
        print('q: quit')
        
        user_choice = get_user_choice()

        if user_choice == '1':
            recipient, amount = get_transaction_value()
            add_transaction(owner, recipient, amount)
        elif user_choice == '2':
            print_blockchain_elements()
        elif user_choice == 'h':
            if len(blockchain) >= 1:
                blockchain[0] = [2]
        elif user_choice == 'q':
            sys.exit()
