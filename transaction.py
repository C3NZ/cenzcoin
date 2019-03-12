# std lib imports
from collections import OrderedDict

# Own imports
from printable import Printable

class Transaction(Printable):
    '''
        Transaction class to represent a transaction to the user

        Properties:
            :sender: the transaction sender
            :recipient: the transaction recipient
            :amount: the transaction amount

        Functions:
            :to_ordered_dict: return the transaction as an ordered dict (primarily for hashing)
    '''
    def __init__(self, sender, recipient, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount

    def to_ordered_dict(self):
        '''
            Convert the transaction into an ordered dict

            Returns:
                An Ordered dict containing key transaction information
        '''
        return OrderedDict([('sender', self.sender), ('recipient', self.recipient), ('amount', self.amount)])
