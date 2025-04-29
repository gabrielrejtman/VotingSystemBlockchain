import hashlib
import json
from validate_docbr import CPF
from fastapi import FastAPI
from pydantic import BaseModel
import json
import requests

from block import Block
from blockchain import Blockchain

cpf = CPF()


class VoteRequest(BaseModel):
    choice: str
    voter_cpf: str

DIFFICULTY = 3

app = FastAPI()
blockchain = Blockchain(DIFFICULTY)
categories = list(blockchain.get_categories())
peers = set()

@app.get("/chain")
def get_chain():
    return blockchain.get_chain()

@app.get("/result")
def get_sorted_votes():
    votes = blockchain.get_votes()
    return sorted(votes.items(), key=lambda x: x[1], reverse=True)

@app.get("/categories")
def get_categories():
    return categories

@app.get("/download")
def export_blockchain():
    chain = blockchain.get_chain()
    return json.dumps(chain, indent=4)

@app.get("/stats")
def get_votes_dataframe():
    votes = blockchain.get_votes()
    return votes

@app.post("/candidate")
def add_candidate(new_category):
    global categories

    if new_category and new_category not in categories:
        categories.append(new_category)
        categories.sort()

        return True, f"Categoria {new_category} adicionada."
    else:
        return False, "Categoria inválida ou já existente"

@app.post("/vote")
def validate_and_vote(vote: VoteRequest):

    print("CHEGOU")
    choice = vote.choice
    voter_cpf = vote.voter_cpf

    print("VARIAVEIS")

    if not categories:
        return {"success": False, "message": "Nenhuma categoria cadastrada."}
    print("SIM CATEGORIAS")

    if not cpf.validate(voter_cpf):
        return {"success": False, "message": "CPF inválido!"}
    print("SIM CPF")

    voter_id_hash = hashlib.sha256(str(voter_cpf).encode()).hexdigest()

    if blockchain.has_user_voted(voter_id_hash):
        return {"success": False, "message": "Você já votou! (' - ';)"}
    
    print("SIM NAO VOTOU")

    blockchain.add_block({"voto": choice}, voter_id_hash)

    print("SIM BLOCKCHAIN")
    return {"success": True, "message": "Voto registrado com sucesso!"}

@app.get("/peers")
def list_peers():
    return {"peers": list(peers)}

@app.get("/peers/sync")
def sync_with_peers():
    global blockchain
    longest_chain = blockchain.get_chain()
    for peer in peers:
        try:
            response = requests.get(f"{peer}/export")
            peer_chain = response.json()
            if len(peer_chain) > len(longest_chain):
                longest_chain = peer_chain
        except Exception as e:
            print(f"Erro ao sincronizar com {peer}: {e}")
            continue

    if len(longest_chain) > len(blockchain.get_chain()):
        new_chain = []
        for block_data in longest_chain:
            new_block = Block(
                index=block_data['_Block__index'],
                timestamp=block_data['_Block__timestamp'],
                candidate=block_data['_Block__candidate'],
                prev_hash=block_data['_Block__prev_hash'],
                voter_hash=block_data['_Block__voter_hash']
            )
            new_block.set_nonce_and_hash(block_data['_Block__nonce'], block_data['_Block__hash'])
            new_chain.append(new_block)

        blockchain.set_chain(new_chain)  # forçar substituição da cadeia
        blockchain.save_to_file()
        global categories
        categories = list(blockchain.get_categories())
        return {"message": "Blockchain sincronizada com sucesso!"}

    return {"message": "Nenhuma cadeia mais longa encontrada."}

@app.post("/peers/register")
def register_peer(peer_url: str):
    peers.add(peer_url)
    return {"peers": list(peers)}

@app.get("/export")
def export_chain():
    return [block for block in blockchain.get_chain()]
