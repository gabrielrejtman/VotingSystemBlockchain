import os
from collections import defaultdict

from block import Block
from time import time
import json

FILENAME = "blockchain.json"


def is_new_block_valid(block, previous_block):
    return (block
            and previous_block
            and previous_block.get_index() + 1 == block.get_index()
            and block.get_prev_hash() == previous_block.get_hash()
            and block.get_hash() == block.compute_hash())


class Blockchain:
    def __init__(self, difficulty):
        self.__difficulty = difficulty
        self.__chain = []
        self.__start_blockchain()

    def __get_latest_block(self):
        return self.__chain[-1]

    def __create_genesis_block(self):
        genesis_block = Block(0, time(), "0", None, None)
        genesis_block.proof_of_work(self.__difficulty)
        self.__chain.append(genesis_block)

        print("Bloco gênesis criado.")

    def __is_blockchain_valid(self):
        def is_genesis_block_valid():
            genesis_block = self.__chain[0]
            return (genesis_block
                    and genesis_block.get_index() == 0
                    and genesis_block.get_prev_hash() is None
                    and genesis_block.get_hash() == genesis_block.compute_hash())
        if not is_genesis_block_valid():
            return False

        for i in range(1, len(self.__chain)):
            if not is_new_block_valid(self.__chain[i], self.__chain[i - 1]):
                return False

        return True

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

        self.__chain = []
        for block_data in loaded_chain:
            block = Block(
                index=block_data['_Block__index'],
                timestamp=block_data['_Block__timestamp'],
                candidate=block_data['_Block__candidate'],
                prev_hash=block_data['_Block__prev_hash'],
                voter_hash=block_data['_Block__voter_hash']
            )
            block.set_nonce_and_hash(block_data['_Block__nonce'], block_data['_Block__hash'])
            self.__chain.append(block)

        print("Blockchain carregada com sucesso.")


    def __start_blockchain(self):
        try:
            self.load_from_file()
            self.__is_blockchain_valid()
        except FileNotFoundError:
            self.__create_genesis_block()

    def __new_block(self, data, voter_hash):
        latest_block = self.__get_latest_block()
        return Block(latest_block.get_index() + 1, time(), data, latest_block.get_hash(), voter_hash)

    def add_block(self, data, voter_hash):
        print("Data", data)
        print("Voter_hash:", voter_hash)

        new_block = self.__new_block(data, voter_hash)

        print("New block:", new_block)

        if new_block and is_new_block_valid(new_block, self.__get_latest_block()):
            print("Entrou em new_block")
            new_block.proof_of_work(self.__difficulty)
            self.__chain.append(new_block)

        print("Bloco adicionado à blockchain.")

        self.save_to_file()

    def get_chain(self):
        return [vars(block) for block in self.__chain]
    
    def set_chain(self, chain):
        self.__chain = chain

    def get_categories(self):
        categories = set()
        for block in self.__chain:
            if isinstance(block.get_data(), dict):
                categories.add(block.get_data()["voto"])

        return categories

    def get_votes(self):
        votes = defaultdict(int)

        for block in self.__chain:
            if isinstance(block.get_data(), dict):
                votes[block.get_data()["voto"]] += 1

        return votes

    def has_user_voted(self, voter_hash):
        for block in self.__chain:
            if block.get_voter_hash() == voter_hash:
                return True
        
        return False
