import os
from collections import defaultdict

from block import Block
from time import time
import json

FILENAME = "blockchain.json"


def is_new_block_valid(block, previous_block):
    return (block
            and previous_block
            and previous_block.index + 1 == block.index
            and block.prev_hash == previous_block.hash
            and block.hash == block.compute_hash())


class Blockchain:
    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.chain = []
        self.start_blockchain()

    def get_latest_block(self):
        return self.chain[-1]

    def start_blockchain(self):
        try:
            self.load_from_file()
        except FileNotFoundError:
            self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, time(), "0", None, None)
        genesis_block.proof_of_work(self.difficulty)
        self.chain.append(genesis_block)

        print("Bloco gênesis criado.")

    def new_block(self, data, voter_hash):
        latest_block = self.get_latest_block()
        return Block(latest_block.index + 1, time(), data, latest_block.hash, voter_hash)

    def add_block(self, data, voter_hash):
        new_block = self.new_block(data, voter_hash)

        if new_block and is_new_block_valid(new_block, self.get_latest_block()):
            new_block.proof_of_work(self.difficulty)
            self.chain.append(new_block)

        print("Bloco adicionado à blockchain.")

        self.save_to_file()

    def get_chain(self):
        return [vars(block) for block in self.chain]

    def get_categories(self):
        categories = set()
        for block in self.chain:
            if isinstance(block.data, dict):
                categories.add(block.data["voto"])

        return categories

    def get_votes(self):
        votes = defaultdict(int)

        for block in self.chain:
            if isinstance(block.data, dict):
                votes[block.data["voto"]] += 1

        return votes

    def has_user_voted(self, voter_hash):
        for block in self.chain:
            if block.get_voter_hash() == voter_hash:
                return True
        
        return False

    def save_to_file(self):
        blockchain_json = json.dumps(self.get_chain(), indent=4)

        try:
            with open(FILENAME, "w") as file:
                file.write(blockchain_json)
        except (FileNotFoundError, ValueError):
            with open(FILENAME, "w") as file:
                file.write(blockchain_json)
        print("Blockchain salva com sucesso.")

    def load_from_file(self):
        if not os.path.exists(FILENAME):
            print("Arquivo não encontrado.")
            raise FileNotFoundError

        with open(FILENAME, "r") as file:
            loaded_chain = json.load(file)

        self.chain = []
        for block_data in loaded_chain:
            block = Block(
                index=block_data['index'],
                timestamp=block_data['timestamp'],
                data=block_data['data'],
                prev_hash=block_data['prev_hash'],
                voter_hash=block_data['voter_hash']
            )
            block.nonce = block_data['nonce']
            block.hash = block_data['hash']
            self.chain.append(block)

        print("Blockchain carregada com sucesso.")
