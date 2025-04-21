import streamlit as st
import hashlib
import json
import time
import pandas as pd
from collections import defaultdict

# Simulação da Blockchain
class Block:
    def __init__(self, index, data, prev_hash):
        self.index = index
        self.timestamp = time.time()
        self.data = data
        self.prev_hash = prev_hash
        self.hash = self.compute_hash()
    
    def compute_hash(self):
        block_string = json.dumps({
            'index': self.index,
            'timestamp': self.timestamp,
            'data': self.data,
            'prev_hash': self.prev_hash
        }, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()
    
    def create_genesis_block(self):
        genesis_block = Block(0, {"msg": "Bloco Gênesis"}, "0")
        self.chain.append(genesis_block)

    def add_block(self, data):
        prev_block = self.chain[-1]
        new_block = Block(len(self.chain), data, prev_block.hash)
        self.chain.append(new_block)

    def get_chain(self):
        return [vars(block) for block in self.chain]

# Dados Simulados (Backend)
if 'blockchain' not in st.session_state:
    st.session_state.blockchain = Blockchain()

if 'categories' not in st.session_state:
    st.session_state.categories = []

if 'votes' not in st.session_state:
    st.session_state.votes = defaultdict(int)

# Streamlit UI
st.title("Sistema de Votação Eletrônica com Blockchain")

menu = st.sidebar.radio("Escolha uma ação:", [
    "Adicionar categoria",
    "Votar",
    "Ver resultados",
    "Ver gráfico de votação",
    "Ver blockchain"
])

# Frontend
if menu == "Adicionar categoria":
    cat = st.text_input("Nova categoria")
    if st.button("Adicionar"):
        if cat and cat not in st.session_state.categories:
            st.session_state.categories.append(cat)
            st.success(f"Categoria '{cat}' adicionada.")
        else:
            st.warning("Categoria inválida ou já existente.")

elif menu == "Votar":
    if not st.session_state.categories:
        st.warning("Adicione categorias antes de votar.")
    else:
        choice = st.selectbox("Escolha uma categoria para votar:", st.session_state.categories)
        if st.button("Votar"):
            st.session_state.votes[choice] += 1
            # Simula gravação no blockchain
            st.session_state.blockchain.add_block({"voto": choice})
            st.success(f"Voto para '{choice}' registrado.")

elif menu == "Ver resultados":
    if st.session_state.votes:
        sorted_votes = sorted(st.session_state.votes.items(), key=lambda x: x[1], reverse=True)
        for cat, count in sorted_votes:
            st.write(f"{cat}: {count} voto(s)")
    else:
        st.info("Nenhum voto registrado ainda.")

elif menu == "Ver gráfico de votação":
    if st.session_state.votes:
        df = pd.DataFrame.from_dict(st.session_state.votes, orient='index', columns=['Votos'])
        st.bar_chart(df)
    else:
        st.info("Nenhum voto registrado ainda.")

elif menu == "Ver blockchain":
    st.write("Histórico da blockchain:")
    chain_data = st.session_state.blockchain.get_chain()
    
    for block in chain_data:
        st.json(block)
    
    blockchain_json = json.dumps(chain_data, indent=4)
    
    st.download_button(
        label="Baixar Blockchain (.json)",
        data=blockchain_json,
        file_name="blockchain_data.json",
        mime="application/json"
    )
        