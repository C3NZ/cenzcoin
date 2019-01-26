import sys

# Mining reward for users mining blocks
MINING_REWARD = 10

# Initialize our (empty) blockchain list
genesis_block = {
        'previous_hash': 'genesis', 
        'index': 0, 
        'transactions': []
    }

# Initialize some other global variables
blockchain = [genesis_block]
open_transactions = []
owner = 'cenz'
participants = {owner}

def hash_block(block):
    '''
        Hash a block and then returned the hashed block to the user

        Arguments:
            :block: The block to be hashed
    '''
    return '-'.join([str(block[key]) for key in block])

def get_balance(participant):
    '''
        Gets the total balance of a single participants

        Arguments:
            :participant: the name of the participant that we want the balance of
    '''

    # Get the total transactions where the participant is the sender (both open and closed)
    tx_sent = [[tx['amount'] for tx in block['transactions'] if tx['sender'] == participant] for block in blockchain]
    open_tx_sent = [[tx['amount'] for tx in open_transactions if tx['sender'] == participant]]
    tx_sent.extend(open_tx_sent)
    amount_sent = 0

    # Sum up the amount the participant has sent
    for tx_amount in tx_sent:
        if len(tx_amount) > 0:
            amount_sent += tx_amount[0]

    # Get the total transactions where the participant is the receiver (strictly closed)
    tx_received = [[tx['amount'] for tx in block['transactions'] if tx['recipient'] == participant] for block in blockchain]
    amount_received = 0

    # Sum up the amount the participant has received
    for tx_amount in tx_received:
        if len(tx_amount) > 0:
            amount_received += tx_amount[0]

    return amount_received - amount_sent

def get_last_blockchain_value():
    '''
        Returns the last value of the current blockchain.
    '''
    if len(blockchain) < 1:
        return None
    else:
        return blockchain[-1]

def verify_transaction(transaction):
    '''
        Veryify that the participant has a high enough balance in order to complete
        a transaction

        Arguments:
            :transacation: The transaction that we're trying to verify
    '''
    sender_balance = get_balance(transaction['sender'])

    return sender_balance >= transaction['amount']


def add_transaction(sender, recipient, amount=1.0):
    '''
        Append a new value as well as the last blockcahin value to the block chain

        Arguments:
                :sender: The sender of the coins
                :recipient: The recipient of the coins.
                :amount: The amount of coins sent with the transaction(default=1.0)
    '''

    transaction = {'sender': sender, 'recipient': recipient, 'amount': amount}

    # If the transaction is legitimate, add it to the open transactions list and
    # keep track of participants
    if verify_transaction(transaction):
        open_transactions.append(transaction)
        # Keep track of all participants
        participants.add(sender)
        participants.add(recipient)
        return True

    return False

def mine_block():
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)
    print(hashed_block)

    # Rewarding the owner for mining a block
    reward_transaction = {
        'sender': 'MINING',
        'recipient': owner,
        'amount': MINING_REWARD
    }
    # Modify a local list of transactions so that users don't get rewarded if 
    # mining turns out to be unsuccessful
    copied_transactions = open_transactions[:]
    copied_transactions.append(reward_transaction)

    block = {
        'previous_hash': hashed_block, 
        'index': len(blockchain), 
        'transactions': copied_transactions
    }

    blockchain.append(block)
    return True


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
    global open_transactions

    while waiting_for_input:
        print('Please choose')
        print('1: Add a new transaction value')
        print('2: Mine a new block')
        print('3: Output the blockchain blocks')
        print('4: Show all participants')
        print('h: Manipulate the chain')
        print('q: quit')

        user_choice = get_user_choice()

        if user_choice == '1':
            recipient, amount = get_transaction_value()
            if add_transaction(owner, recipient, amount):
                print('Added transaction!')
            else:
                print('Transaction failed')
        elif user_choice == '2':
            if mine_block():
                open_transactions = []
        elif user_choice == '3':
            print_blockchain_elements()
        elif user_choice == '4':
            print(participants)
        elif user_choice == 'h':
            if len(blockchain) >= 1:
                blockchain[0] = {
                    'previous_hash': '',
                    'index': 0,
                    'transactions': [{'sender': 'tim', 'recipient': 'cenz', 'amount': 20}]
                }
        elif user_choice == 'q':
            waiting_for_input = False

        print(get_balance(owner))
        # Verify the blockchain over every action
        if not verify_chain():
            print_blockchain_elements()
            print('Invalid blockchain!')
            break
    print('Blockchain now shutting down')

if __name__ == '__main__':
    main()
