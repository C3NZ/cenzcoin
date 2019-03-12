import hashlib as hl
import json

def hash_string_256(input_string):
    '''
        Hash a string using the sha256 algorithim

        Returns:
            a string containing the hex digest of a sha256 hash
    '''
    return hl.sha256(input_string).hexdigest()

def hash_block(block):
    '''
        Hash a block and then returned the hashed block to the user

        Arguments:
            :block: The block to be hashed

        Returns:
            a string containing the hex digest of the sha 256 hash
    '''
    # Stringify and encode the block, return sha 256
    stringified_block = json.dumps(block).encode()
    return hash_string_256(stringified_block)


