import streamlit as st

import backend

def frontend(blockchain, categories, votes):
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

        if st.button("Votar"):
            success, message = backend.add_candidate(categories, category)

            if success:
                st.success(message)
            else:
                st.warning(message)

    elif menu == "Votar":
        if not categories:
            st.warning("Adicione um canditato antes de votar.")
        else:
            choice = st.selectbox("Escolha um candidato para votar:", categories)
            voter_cpf = st.text_input("Insira seu CPF")

            if st.button("Votar"):
                success, message = backend.validate_and_vote(
                    blockchain, votes, categories, choice, voter_cpf
                )

                if success:
                    st.success(message)
                else:
                    st.warning(message)

    elif menu == "Ver resultados":
        if votes:
            sorted_votes = backend.get_sorted_votes(votes)

            for cat, count in sorted_votes:
                st.write(f"{cat}: {count} voto" + ("s" if count > 1 else ""))

        else:
            st.info("Nenhum voto registrado ainda.")

    elif menu == "Ver gráfico da votação":
        if votes:
            df = backend.get_votes_dataframe(votes)
            st.bar_chart(df)
        else:
            st.info("Nenhum voto registrado ainda.")

    elif menu == "Visualizar blockchain":
        st.write("Histórico da blockchain:")
        chain = blockchain.get_chain()

        for block in chain:
            st.json(block)

        blockchain_json = backend.export_blockchain(chain)

        st.download_button(
            label="Baixar Blockchain (.json)",
            data=blockchain_json,
            file_name="blockchain.json",
            mime="application/json"
        )