import sys

# Initialize our (empty) blockchain list
genesis_block = {
        'previous_hash': 'genesis', 
        'index': 0, 
        'transacations': []
    }

blockchain = [genesis_block]
open_transactions = []
owner = 'cenz'

def hash_block(block):
    '''
        Hash a block and then returned the hashed block to the user

        Arguments:
            :block: The block to be hashed
    '''
    return '-'.join([str(block[key]) for key in block])

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
    last_block = blockchain[-1]
   
    hashed_block = hash_block(last_block)
    print(hashed_block)
    
    block = {
        'previous_hash': hashed_block, 
        'index': len(blockchain), 
        'transacations': open_transactions
    }
    blockchain.append(block)


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

    # Enumerate the blockchain in order to retrieve the current block & it's index
    for index, block in enumerate(blockchain):
        if index == 0:
            continue

        # Ensure the current blocks previous hash matches the hash of the previous block
        if block['previous_hash'] != hash_block(blockchain[index - 1]):
            return False
    return True



def main():
    waiting_for_input = True

    while waiting_for_input:
        print('Please choose')
        print('1: Add a new transaction value')
        print('2: Mine a new block')
        print('3: Output the blockchain blocks')
        print('h: Manipulate the chain')
        print('q: quit')

        user_choice = get_user_choice()

        if user_choice == '1':
            recipient, amount = get_transaction_value()
            add_transaction(owner, recipient, amount)
            print(open_transactions)
        elif user_choice == '2':
            mine_block()
        elif user_choice == '3':
            print_blockchain_elements()
        elif user_choice == 'h':
            if len(blockchain) >= 1:
                blockchain[0] = {
                    'previous_hash': '',
                    'index': 0,
                    'transactions': [{'sender': 'tim', 'recipient': 'cenz', 'amount': 20}]
                }
        elif user_choice == 'q':
            waiting_for_input = False

        # Verify the blockchain over every action
        if not verify_chain():
            print_blockchain_elements()
            print('Invalid blockchain!')
            break

    print('Blockchain now shutting down')

if __name__ == '__main__':
    main()
