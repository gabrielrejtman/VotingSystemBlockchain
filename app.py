import hashlib
import json
import re

import matplotlib.pyplot as plt
import os

import streamlit as st
from dotenv import load_dotenv
from matplotlib.ticker import MaxNLocator
from web3 import Web3
from validate_docbr import CPF

from messages import get_languages
from messages import Messages

load_dotenv()

# Initial setup
infura_url = os.getenv("INFURA_URL")
web3 = Web3(Web3.HTTPProvider(infura_url))

contract_address = Web3.to_checksum_address(os.getenv("CONTRACT_ADDRESS"))
with open("voting_abi.json", "r") as f:
    contract_abi = json.load(f)

contract = web3.eth.contract(address=contract_address, abi=contract_abi)

private_key = os.getenv("PRIVATE_KEY")
account_address = web3.eth.account.from_key(private_key).address

# Settings Streamlit UI

st.set_page_config(
    page_title="DApp Voting System",
    page_icon="🗳️",
    layout="centered",  # ou "wide"
    initial_sidebar_state="expanded"
)

available_languages = get_languages()
language = st.sidebar.selectbox("🌐", available_languages)
msg = Messages(language)

st.title(msg.TITLES.MAIN)

menu_options = [
    msg.MENU_OPTIONS.ADD_CANDIDATE,
    msg.MENU_OPTIONS.VOTE,
    msg.MENU_OPTIONS.VIEW_RESULTS,
    msg.MENU_OPTIONS.VIEW_CHART
]
option = st.sidebar.selectbox(msg.MENU_OPTIONS.MENU_NAVIGATION, menu_options)

msg.set_language(language)

if option == msg.MENU_OPTIONS.ADD_CANDIDATE:
    name = st.text_input(msg.LABELS.CANDIDATE_NAME)
    if st.button(msg.BUTTONS.ADD):
        if not name.strip():
            st.warning(msg.WARNINGS.EMPTY_CANDIDATE_FIELD)
        else:
            # Obtém todos os nomes de candidatos do contrato
            existing_names = contract.functions.getCandidateNames().call()

            # Verifica se o nome (ignorando maiúsculas/minúsculas e espaços) já está cadastrado
            normalized_input = name.strip().lower()
            name_exists = any(n.strip().lower() == normalized_input for n in existing_names)

            if name_exists:
                st.warning(msg.WARNINGS.CANDIDATE_ALREADY_EXISTS.format(name))
            else:
                nonce = web3.eth.get_transaction_count(account_address)
                base_gas_price = web3.eth.gas_price + web3.to_wei('5', "gwei")
                tx = contract.functions.addCandidate(name).build_transaction({
                    'from': account_address,
                    'nonce': nonce,
                    'gas': 300000,
                    'gasPrice': base_gas_price + web3.to_wei('1', 'gwei')
                })
                signed_tx = web3.eth.account.sign_transaction(tx, private_key)
                tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
                tx_hash_hex = web3.to_hex(tx_hash)
                st.success(msg.SUCCESS.CANDIDATE_ADDED.format(name, tx_hash_hex))

elif option == msg.MENU_OPTIONS.VOTE:
    names = contract.functions.getCandidateNames().call()

    if "vote_in_progress" not in st.session_state:
        st.session_state.vote_in_progress = False

    if names:
        cpf = CPF()
        voter_cpf = st.text_input(msg.LABELS.CPF_INPUT)
        candidate = st.selectbox(msg.LABELS.CANDIDATE_NAME, names)
        candidate_id = names.index(candidate) + 1

        vote_button_disabled = st.session_state.vote_in_progress
        vote_clicked = st.button(msg.BUTTONS.VOTE, disabled=vote_button_disabled)

        if vote_clicked:
            if cpf.validate(voter_cpf):
                cpf_numbers = re.sub(r"\D", "", voter_cpf)
                hash_bytes = hashlib.sha256(cpf_numbers.encode()).digest()
                hash_hex = web3.to_hex(hash_bytes)

                has_voted = contract.functions.hasVoted(hash_hex).call()

                if has_voted:
                    st.warning(msg.WARNINGS.CPF_ALREADY_VOTED)
                else:
                    st.session_state.vote_in_progress = True
                    with st.spinner("Aguarde, seu voto está sendo registrado na blockchain..."):
                        try:
                            nonce = web3.eth.get_transaction_count(account_address, "pending")
                            tx = contract.functions.vote(hash_hex, int(candidate_id)).build_transaction({
                                'from': account_address,
                                'nonce': nonce,
                                'gas': 300000,
                                'gasPrice': web3.to_wei('10', 'gwei')
                            })
                            signed_tx = web3.eth.account.sign_transaction(tx, private_key)
                            tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)

                            # Espera confirmação
                            receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
                            tx_hash_hex = web3.to_hex(tx_hash)

                            st.success(msg.SUCCESS.VOTE_CASTED.format(tx_hash_hex))
                        except Exception as e:
                            st.error(f"Erro ao registrar o voto: {e}")
                        finally:
                            st.session_state.vote_in_progress = False
            elif voter_cpf:
                st.warning(msg.WARNINGS.INVALID_CPF)
            else:
                st.warning(msg.WARNINGS.EMPTY_CPF_FIELD)
    else:
        st.warning(msg.WARNINGS.NO_CANDIDATES)

elif option == msg.MENU_OPTIONS.VIEW_RESULTS:
    names = contract.functions.getCandidateNames().call()
    if names:
        candidate = st.selectbox(msg.LABELS.CANDIDATE_NAME, names)
        candidate_id = names.index(candidate) + 1
        if st.button(msg.BUTTONS.CONSULT):
            name, all_votes = contract.functions.getCandidate(int(candidate_id)).call()
            st.info(msg.RESULTS.CANDIDATE_RESULT.format(name, all_votes))
    else:
        st.warning(msg.WARNINGS.NO_CANDIDATES)

elif option == msg.MENU_OPTIONS.VIEW_CHART:
    count = contract.functions.candidatesCount().call()
    all_candidates = []
    all_votes = []
    for i in range(1, count + 1):
        c, v = contract.functions.getCandidate(i).call()
        all_candidates.append(c)
        all_votes.append(v)

    fig, ax = plt.subplots()
    ax.bar(all_candidates, all_votes, color='royalblue')
    ax.set_xlabel(msg.CHART_LABELS.CANDIDATE)
    ax.set_ylabel(msg.CHART_LABELS.VOTE_COUNT)
    ax.set_title(msg.CHART_LABELS.CHART_TITLE)

    # Remover decimais dos valores do eixo Y
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))

    # Restante do código
    ax.set_xticklabels(all_candidates, rotation=45, ha='right')
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    fig.tight_layout()
    st.pyplot(fig)