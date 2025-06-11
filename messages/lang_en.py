from types import SimpleNamespace


TITLES = SimpleNamespace(
    MAIN="Voting DApp with Blockchain"
)

MENU_OPTIONS = SimpleNamespace(
    MENU_NAVIGATION="Navigate",
    ADD_CANDIDATE="Add candidate",
    VOTE="Vote",
    VIEW_RESULTS="View Results",
    VIEW_CHART="View Chart"
)

SUCCESS = SimpleNamespace(
    VOTE_CASTED="Vote registered!\n\nTX: {}",
    CANDIDATE_ADDED="Candidate '{}' added!\n\nTX: {}"
)

WARNINGS = SimpleNamespace(
    NO_CANDIDATES="No candidates found.\n\nPlease, add candidates before voting.",
    CANDIDATE_ALREADY_EXISTS="Candidate '{}' already registered.",
    EMPTY_CANDIDATE_FIELD="Candidate name cannot be empty!",
    INVALID_CPF="Invalid CPF!",
    EMPTY_CPF_FIELD="Please, enter your CPF.",
    CPF_ALREADY_VOTED="This CPF has already been used to vote!"
)

RESULTS = SimpleNamespace(
    CANDIDATE_RESULT="🧑 Candidate: {}\n\n🗳️ Votes: {}"
)

LABELS = SimpleNamespace(
    CANDIDATE_NAME="Candidate name",
    CPF_INPUT="Enter your CPF (it will not be linked to your vote)",
    CHOOSE_CANDIDATE="Choose a candidate",
)

BUTTONS = SimpleNamespace(
    ADD="Add Candidate",
    VOTE="Vote",
    CONSULT="Consult"
)

CHART_LABELS = SimpleNamespace(
    CANDIDATE="Candidates",
    VOTE_COUNT="Count of Votes",
    CHART_TITLE="Voting Results"
)
