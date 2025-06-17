from types import SimpleNamespace


TITLES = SimpleNamespace(
    MAIN="DApp de Votação com Blockchain",
)

MENU_OPTIONS = SimpleNamespace(
    MENU_NAVIGATION="Navegar",
    ADD_CANDIDATE="Adicionar Candidato",
    VOTE="Votar",
    VIEW_RESULTS="Visualizar Resultados",
    VIEW_CHART="Gráfico de Resultados"
)

SUCCESS = SimpleNamespace(
    VOTE_CASTED="Voto computado!\n\nTX: {}",
    CANDIDATE_ADDED="Candidato '{}' adicionado!\n\nTX: {}"
)

WARNINGS = SimpleNamespace(
    NO_CANDIDATES="Nenhum candidato cadastrado.\n\nPor favor, adicione candidatos antes de votar.",
    CANDIDATE_ALREADY_EXISTS="O candidato {} já está cadastrado.",
    EMPTY_CANDIDATE_FIELD="O nome do candidato não pode estar em branco.",
    INVALID_CPF="CPF inválido!",
    EMPTY_CPF_FIELD="Por favor, insira o seu CPF.",
    CPF_ALREADY_VOTED="Esse CPF já foi usado para votar.",
    NOT_OWNER="O usuário atual não é o owner do contrato"
)

RESULTS = SimpleNamespace(
    CANDIDATE_RESULT="🧑 Candidato: {}\n\n🗳️ Votos: {}"
)

LABELS = SimpleNamespace(
    CANDIDATE_NAME="Nome do candidato",
    CPF_INPUT="Digite seu CPF (ele não será vínculado ao seu voto)",
    CHOOSE_CANDIDATE="Escolha um candidato",
    CONSULT_BUTTON="Consultar"
)

BUTTONS = SimpleNamespace(
    ADD="Adicionar Candidato",
    VOTE="Votar",
    CONSULT="Consultar"
)

CHART_LABELS = SimpleNamespace(
    CANDIDATE="Candidatos",
    VOTE_COUNT="Contagem de Votos",
    CHART_TITLE="Resultado da Votação"
)
