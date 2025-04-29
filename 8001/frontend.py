import streamlit as st
import requests
import pandas as pd

import backend

API_URL = "http://127.0.0.1:8001"

def frontend():
    def categories():
        return backend.get_categories()
    
    def votes():
        return backend.get_sorted_votes()
    
    st.title("Sistema de Votação Eletrônica com Blockchain")

    menu = st.sidebar.radio("Escolha uma ação:", [
        "Adicionar candidato",
        "Votar",
        "Ver resultados",
        "Ver gráfico da votação",
        "Visualizar blockchain"
    ])

    if menu == "Adicionar candidato":
        category = st.text_input("Novo candidato")

        if st.button("Adicionar candidato"):
            # success, message = backend.add_candidate(category)
            response = requests.post(f"{API_URL}/candidate")

            if response.status_code == 200:
                st.success("Candidato adicionado com sucesso")
            else:
                st.warning("Candidato não é válido")

    elif menu == "Votar":
        if not categories():
            st.warning("Adicione um canditato antes de votar.")
        else:
            choice = st.selectbox("Escolha um candidato para votar:", categories())
            voter_cpf = st.text_input("Insira seu CPF")

            if st.button("Votar"):
                # success, message = backend.validate_and_vote(choice, voter_cpf)
                # success, message = requests.post(f"{API_URL}/vote")
                response = requests.post(
                    f"{API_URL}/vote",
                    json={
                        "choice":choice,
                        "voter_cpf":voter_cpf
                    }
                )

                result = response.json()
                success = result['success']
                message = result['message']

                if response.status_code == 200 and success:
                    st.success(message)
                else:
                    st.warning(message)

    elif menu == "Ver resultados":
        if votes():
            # sorted_votes = backend.get_sorted_votes()
            response = requests.get(f"{API_URL}/result")
            sorted_votes = response.json()

            for cat, count in sorted_votes:
                st.write(f"{cat}: {count} voto" + ("s" if count > 1 else ""))

        else:
            st.info("Nenhum voto registrado ainda.")

    elif menu == "Ver gráfico da votação":
        if votes():
            # df = backend.get_votes_dataframe()
            response = requests.get(f"{API_URL}/stats")
            data = response.json()
            print("DATA:", data)
            df = pd.DataFrame.from_dict(data, orient='index', columns=['Votos'])
            st.bar_chart(df)
        else:
            st.info("Nenhum voto registrado ainda.")

    elif menu == "Visualizar blockchain":
        st.write("Histórico da blockchain:")
        # chain = backend.get_chain()
        response = requests.get(f"{API_URL}/chain")

        chain = response.json()

        print(chain)

        for block in chain:
            st.json(block)

        blockchain_json = backend.export_blockchain()

        st.download_button(
            label="Baixar Blockchain (.json)",
            data=blockchain_json,
            file_name="blockchain.json",
            mime="application/json"
        )


        peer_url = st.text_input("Digite o endereço do peer (ex: http://localhost:8001)")
        if st.button("Registrar"):
            if peer_url:
                response = requests.post(f"{API_URL}/peers/register?peer_url={peer_url}")
                st.json(response.json())
            else:
                st.warning("Você precisa digitar um endereço!")


        if st.button("Sincronizar"):
            response = requests.get(f"{API_URL}/peers/sync")
            st.json(response.json())

            # Exemplo de execução
            # asyncio.run(register_peer())
            # asyncio.run(sync_peers())
