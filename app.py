import streamlit as st
from web3 import Web3
from dotenv import load_dotenv
import os
import json

# Carrega as variáveis do .env
load_dotenv()

# Conecta à Sepolia via Infura
infura_url = os.getenv("INFURA_URL")
print(infura_url)
web3 = Web3(Web3.HTTPProvider(infura_url))

if not web3.is_connected():
    st.error("Não foi possível conectar à blockchain.")
    st.stop()

# Carrega a ABI do contrato
with open("contract_abi.json", "r") as f:
    abi = json.load(f)

# Endereço do contrato e da conta
contract_address = Web3.to_checksum_address(os.getenv("CONTRACT_ADDRESS"))
contract = web3.eth.contract(address=contract_address, abi=abi)

private_key = os.getenv("PRIVATE_KEY")
account = web3.eth.account.from_key(private_key)
sender_address = account.address

candidate_list = ["Alice", "Bob", "Carol"]

st.title("🗳️ Sistema de Votação Blockchain")

# Exibe opções de candidatos
candidato = st.selectbox("Escolha um candidato:", candidate_list)



cpf = st.text_input("CPF")

if st.button("Votar"):
    try:
        # Pega o nonce atual para a conta
        nonce = web3.eth.get_transaction_count(sender_address)

        # Pega o gasPrice atual e incrementa 10% para evitar erro replacement transaction underpriced
        gas_price = web3.eth.gas_price
        gas_price = int(gas_price * 1.1)  # incrementa 10%

        tx = contract.functions.vote(candidate_list.index(candidato), cpf).build_transaction({
            "from": sender_address,
            "nonce": nonce,
            "gas": 200000,
            "gasPrice": gas_price
        })

        signed_tx = account.sign_transaction(tx)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

        st.success(f"Voto enviado com sucesso! TX Hash: {tx_hash.hex()}")
    except Exception as e:
        st.error(f"Erro ao enviar voto: {e}")

# Ver votos (função view do contrato)
if st.button("Ver resultados"):
    try:
        votos_alice = contract.functions.get_votes(1).call()
        votos_bob = contract.functions.get_votes(2).call()
        votos_carol = contract.functions.get_votes(3).call()

        st.write(f"Alice: {votos_alice} votos")
        st.write(f"Bob: {votos_bob} votos")
        st.write(f"Carol: {votos_carol} votos")
    except Exception as e:
        st.error(f"Erro ao obter votos: {e}")
