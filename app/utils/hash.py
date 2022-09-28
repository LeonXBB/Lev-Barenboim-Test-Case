import hashlib

def get_hash(string: str) -> str:
    '''
    Easy function to return hash of a given string: str. Easier that built-in syntax.
    '''
    return hashlib.sha256(string.encode('utf-8')).hexdigest()