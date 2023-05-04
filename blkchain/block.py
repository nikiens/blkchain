import random
import string
import json

from hashlib import sha256

class Block():

    def __init__(self, index, prev_hash, nonce_type, node_id):
        self.index = index
        self.prev_hash = prev_hash
        self.hash = self.generate_hash(nonce_type)
        self.data = self.generate_random_string(256)
        self.nonce = 0
        self.node_id = node_id

    def generate_random_string(self, length):
        return ''.join(random.choice(string.ascii_letters) for i in range(length))
    
    def generate_hash(self, nonce_type):
        concat = "".join([str(self.index), self.prev_hash, self.data, str(self.nonce)])
        hash = sha256(concat.encode('utf-8'))

        while hash.hexdigest()[-4:] != '0000':
            self.update_nonce(nonce_type)

            concat = "".join([str(self.index), self.prev_hash, self.data, str(self.nonce)])
            hash = sha256(concat.encode('utf-8'))
        
        self.hash = hash

    def update_nonce(self, type):
        if type == '1to10':
            self.nonce = random.randint(1, 10)
        elif type == '11to20':
            self.nonce = random.randint(11,20)
        elif type == '21to30':
            self.nonce = random.random(21, 30)
        else:
            raise Exception('Wrong nonce type!')
        
    def to_json(self):
        return json.dumps(self.__dict__)
    
    def __str__(self):
        return \
            f'ID = {self.index}\t' + \
            f'Prev Hash = {self.prev_hash}\t' + \
            f'Hash = {self.hash}\t' + \
            f'Data = {self.data}\t' + \
            f'Nonce = {self.nonce}\t' + \
            f'Node ID = {self.node_id}'