import json
import hashlib


class Block:
    def __init__(self, index, timestamp, data, prev_hash, voter_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.prev_hash = prev_hash
        self.nonce = 0
        self.hash = self.compute_hash()
        self.voter_hash = voter_hash

    def compute_hash(self):
        block_string = json.dumps({
            'index': self.index,
            'timestamp': self.timestamp,
            'data': self.data,
            'prev_hash': self.prev_hash,
            'nonce': self.nonce
        }, sort_keys=True).encode()
        generated_hash = hashlib.sha256(block_string).hexdigest()
        print(generated_hash, "Nonce:", self.nonce)

        return generated_hash

    def proof_of_work(self, difficulty):
        target = "0" * difficulty

        while not self.hash.startswith(target):
            self.nonce += 1
            self.hash = self.compute_hash()

    def get_voter_hash(self):
        return self.voter_hash
