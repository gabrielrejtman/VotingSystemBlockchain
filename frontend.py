import streamlit as st
import requests
import pandas as pd

import backend

API_URL = "http://127.0.0.1:8000"

def frontend():
    def categories():
        response = requests.get(f"{API_URL}/categories")
        return response.json()
    
    def votes():
        response = requests.get(f"{API_URL}/result")
        return response.json()
    
    st.title("Eletronic Voting System With Blockchain")

    menu = st.sidebar.radio("Choose an action:", [
        "Add candidate",
        "Vote",
        "See results",
        "See election's graphic",
        "See blockchain"
    ])

    if menu == "Add candidate":
        category = st.text_input("New candidate")

        if st.button("Add candidate"):
            response = requests.post(f"{API_URL}/candidate")

            if response.status_code == 200:
                st.success("The candidate has been added")
            else:
                st.warning("Invalid candidate")

    elif menu == "Vote":
        if not categories():
            st.warning("Add a candidate before voting")
        else:
            choice = st.selectbox("Choose a candidate to vote", categories())
            voter_cpf = st.text_input("Insert your CPF")

            if st.button("Vote"):
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

    elif menu == "See results":
        if votes():
            response = requests.get(f"{API_URL}/result")
            sorted_votes = response.json()

            for cat, count in sorted_votes:
                st.write(f"{cat}: {count} voto" + ("s" if count > 1 else ""))

        else:
            st.info("The are no votes yet.")

    elif menu == "See election's graphic":
        if votes():
            response = requests.get(f"{API_URL}/stats")
            data = response.json()
            print("DATA:", data)
            df = pd.DataFrame.from_dict(data, orient='index', columns=['Votos'])
            st.bar_chart(df)
        else:
            st.info("There are no votes yet.")

    elif menu == "See blockchain":
        st.write("Blockchain's history:")
        response = requests.get(f"{API_URL}/chain")

        chain = response.json()

        print(chain)

        for block in chain:
            st.json(block)

        blockchain_json = backend.export_blockchain()

        st.download_button(
            label="Download Blockchain (.json)",
            data=blockchain_json,
            file_name="blockchain.json",
            mime="application/json"
        )


        peer_url = st.text_input("Insert the peer's address (e.g: http://localhost:8001)")
        if st.button("Register"):
            if peer_url:
                response = requests.post(f"{API_URL}/peers/register?peer_url={peer_url}")
                st.json(response.json())
            else:
                st.warning("You have to type an address!")


        if st.button("Synchronize"):
            response = requests.get(f"{API_URL}/peers/sync")
            st.json(response.json())
