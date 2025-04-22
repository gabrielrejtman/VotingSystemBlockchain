from block import Block
from time import time


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
        self.create_genesis_block()

    def get_latest_block(self):
        return self.chain[-1]

    def create_genesis_block(self):
        genesis_block = Block(0, time(), "0", None)
        genesis_block.proof_of_work(self.difficulty)
        self.chain.append(genesis_block)

        print("Bloco gênesis criado.")

    def new_block(self, data):
        latest_block = self.get_latest_block()
        return Block(latest_block.index + 1, time(), data, latest_block.hash)

    def add_block(self, data):
        new_block = self.new_block(data)

        if new_block and is_new_block_valid(new_block, self.get_latest_block()):
            new_block.proof_of_work(self.difficulty)
            self.chain.append(new_block)

        print("Bloco adicionado à blockchain.")

    def get_chain(self):
        return [vars(block) for block in self.chain]
