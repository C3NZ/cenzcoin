# std lib imports
from collections import OrderedDict

# Own imports
from util.printable import Printable

class Transaction(Printable):
    '''
        Transaction class to represent a transaction to the user

        Attributes:
            :sender: the transaction sender
            :recipient: the transaction recipient
            :amount: the transaction amount

        Functions:
            :to_ordered_dict: return the transaction as an ordered dict (primarily for hashing)
    '''
    def __init__(self, sender, recipient, signature, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.signature = signature

    def to_ordered_dict(self):
        '''
            Convert the transaction into an ordered dict

            Returns:
                An Ordered dict containing key transaction information
        '''
        # Tx data (used for our order dictionary)
        tx_data = [
            ('sender', self.sender),
            ('recipient', self.recipient),
            ('signature', self.signature),
            ('amount', self.amount)
        ]

        # Return an ordered dict containing the 
        return OrderedDict(tx_data)
