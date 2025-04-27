# VotingSystemBlockchain

This project is an Electronic Voting System built in Python, 
using blockchain to securely record votes and Streamlit for the web interface.
> 🇧🇷 [Versão em Português](./README-pt.md)

## Table of contents
- [Technologies](#technologies)
- [Features](#features)
- [Blockchain in the project](#blockchain-in-the-project)
- [How to run](#how-to-run)

## Technologies
- Python 3.10+
- Streamlit - for creating the web interface
- validate-docbr - for CPF validation
- Pandas - for manipulating and displaying data
- Hashlib - for creating hashes
- JSON - for exporting blockchain data

## Features
- Add new candidates to the voting system
- Vote using CPF (with identity protection)
- Blockchain to securely and immutably record each vote
- View results and chars in real-time
- Export the complete blockchain in .json format
- Prevent duplicate votes

## Blockchain in the project
- Each vote is stored as a new block
- Each block contains:
  - Vote data (voted candidate, voter identification)
  - Timestamp of the voting moment
  - Hash of the previous vote

## How to run
```bash
git clone https://github.com/gabrielrejtman/VotingSystemBlockchain.git
cd VotingSystemBlockchain
pip install -r requirements.txt
streamlit run main.py
