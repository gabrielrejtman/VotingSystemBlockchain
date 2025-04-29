import json
import hashlib


class Block:
    def __init__(self, index, timestamp, candidate, prev_hash, voter_hash):
        self.__index = index
        self.__timestamp = timestamp
        self.__candidate = candidate
        self.__prev_hash = prev_hash
        self.__nonce = 0
        self.__voter_hash = voter_hash
        self.__hash = self.compute_hash()

    def compute_hash(self):
        block_string = json.dumps({
            'index': self.__index,
            'timestamp': self.__timestamp,
            'data': self.__candidate,
            'prev_hash': self.__prev_hash,
            'nonce': self.__nonce
        }, sort_keys=True).encode()
        generated_hash = hashlib.sha256(block_string).hexdigest()
        print(generated_hash, "Nonce:", self.__nonce)

        return generated_hash

    def proof_of_work(self, difficulty):
        target = "0" * difficulty

        while not self.__hash.startswith(target):
            self.__nonce += 1
            self.__hash = self.compute_hash()

    def to_dict(self):
        return {
            "index": self.__index,
            "timestamp": self.__timestamp,
            "candidate": self.__candidate,
            "prev_hash": self.__prev_hash,
            "nonce": self.__nonce,
            "voter_hash": self.__voter_hash,
            "hash": self.__hash
        }

    def __set_index(self, index):
        self.__index = index

    def __set_timestamp(self, timestamp):
        self.__timestamp = timestamp

    def __set_data(self, data):
        self.__candidate = data

    def __set_prev_hash(self, prev_hash):
        self.__prev_hash = prev_hash

    def __set_nonce(self, nonce):
        self.__nonce = nonce

    def __set_hash(self, hash):
        self.__hash = hash

    def set_voter_hash(self, voter_hash):
        self.__voter_hash = voter_hash

    def get_index(self):
        return self.__index

    def get_timestamp(self):
        return self.__timestamp

    def get_data(self):
        return self.__candidate

    def get_prev_hash(self):
        return self.__prev_hash

    def get_nonce(self):
        return self.__nonce

    def get_hash(self):
        return self.__hash

    def get_voter_hash(self):
        return self.__voter_hash

    def set_nonce_and_hash(self, nonce, block_hash):
        self.__set_nonce(nonce)
        self.__set_hash(block_hash)
        