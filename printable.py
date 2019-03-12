'''
    Printable module
'''

class Printable:
    '''
        For objects that are all printable as a dictionary (helper class)
    '''
    def __repr__(self):
        return str(self.__dict__)
