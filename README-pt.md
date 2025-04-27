# VotingSystemBlockchain

Este projeto é um Sistema de Votação Eletrônica construído em Python,
utilizando blockchain para registrar os votos de forma segura e Streamlit para a interface Web.
Este sistema foi desenvolvido para facilitar o processo de votação eletrônica,
garantindo segurança e transparência por meio da tecnologia de <i>blockchain</i>

> 🇺🇸 [English Version](./README.md)

## Sumário
- [Tecnologias](#tecnologias)
- [Funcionalidades](#funcionalidades)
- [A _blockchain_ no projeto](#a-iblockchaini-no-projeto)
- [Como rodar](#como-rodar)

## Tecnologias
- Python 3.10+
- Streamlit - para criar a interface Web
- validate-docbr - para validação de CPF
- Pandas - para manipular e exibir dados
- Hashlib - para a criação de hashes
- JSON - para exportação dos dados da blockchain

## Funcionalidades
- Adicionar novos candidatos à votação
- Votar utilizando o CPF (com proteção de identidade)
- <i>Blockchain</i> para registrar cada voto de forma segura e imutável
- Visualizar resultados e gráficos em tempo real
- Exportar a blockchain completa em formato .json
- Impedir votos duplicados

## A <i>blockchain</i> no projeto
- Cada voto é armazenado como um novo bloco
- Cada bloco contém:
  - Dados do voto (candidato votado, identificação do eleitor)
  - <i>Timestamp</i> do momento da votação
  - <i>Hash</i> do voto anterior

## Como rodar
```bash
git clone https://github.com/gabrielrejtman/VotingSystemBlockchain.git
cd VotingSystemBlockchain
pip install -r requirements.txt
streamlit run main.py
