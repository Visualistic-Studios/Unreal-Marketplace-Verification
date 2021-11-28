from hashlib import sha256



# create hash string from input string

def hash_string(string):
    return sha256(string.encode('utf-8')).hexdigest()



