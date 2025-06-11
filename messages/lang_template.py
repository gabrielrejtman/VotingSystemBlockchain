from types import SimpleNamespace


TITLES = SimpleNamespace(
    MAIN="",
)

MENU_OPTIONS = SimpleNamespace(
    MENU_NAVIGATION="",
    ADD_CANDIDATE="",
    VOTE="",
    VIEW_RESULTS="",
    VIEW_CHART="",
)

SUCCESS = SimpleNamespace(
    VOTE_CASTED="",
    CANDIDATE_ADDED="",
)

WARNINGS = SimpleNamespace(
    NO_CANDIDATES="",
    CANDIDATE_ALREADY_EXISTS="",
    EMPTY_CANDIDATE_FIELD="",
    INVALID_CPF="",
    EMPTY_CPF_FIELD="",
    CPF_ALREADY_VOTED="",
)

RESULTS = SimpleNamespace(
    CANDIDATE_RESULT="",
)

LABELS = SimpleNamespace(
    CANDIDATE_NAME="",
    CPF_INPUT="",
    CHOOSE_CANDIDATE="",
)

BUTTONS = SimpleNamespace(
    ADD="",
    VOTE="",
    CONSULT="",
)

CHART_LABEL = SimpleNamespace(
    CANDIDATE="",
    VOTE_COUNT="",
    CHART_TITLE="",
)
