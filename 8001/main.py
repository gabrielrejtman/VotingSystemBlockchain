import streamlit as st

from blockchain import Blockchain
from frontend import frontend

DIFFICULTY = 3

# Dados Simulados (Backend)
if 'blockchain' not in st.session_state:
    st.session_state.blockchain = Blockchain(DIFFICULTY)

if 'categories' not in st.session_state:
    st.session_state.categories = sorted(st.session_state.blockchain.get_categories())

if 'votes' not in st.session_state:
    st.session_state.votes = st.session_state.blockchain.get_votes()

frontend()