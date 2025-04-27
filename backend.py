import hashlib
import json
import pandas as pd
from validate_docbr import CPF

cpf = CPF()

def add_candidate(categories, new_category):
    if new_category and new_category not in categories:
        categories.append(new_category)
        categories.sort()

        return True, f"Categoria {new_category} adicionada."
    else:
        return False, "Categoria inválida ou já existente"

def validate_and_vote(blockchain, votes, categories, choice, voter_cpf):
    if not categories:
        return False, "Nenhuma categoria cadastrada."

    if not cpf.validate(voter_cpf):
        return False, "CPF inválido!"

    voter_id_hash = hashlib.sha256(str(voter_cpf).encode()).hexdigest()

    if blockchain.has_user_voted(voter_id_hash):
        return False, "Você já votou! (' - ';)"

    votes[choice] += 1

    blockchain.add_block({"voto": choice}, voter_id_hash)
    return True, "Voto registrado com sucesso!"

def get_sorted_votes(votes):
    return sorted(votes.items(), key=lambda x: x[1], reverse=True)

def get_votes_dataframe(votes):
    df = pd.DataFrame.from_dict(votes, orient='index', columns=['Votos'])
    print(df)
    return df

def export_blockchain(blockchain):
    return json.dumps(blockchain, indent=4)