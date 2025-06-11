from . import lang_pt, lang_en

_languages = {
    "English":lang_en,
    "Português":lang_pt
}


def get_languages():
    return _languages.keys()


class Messages:
    def __init__(self, lang="English"):
        lang_module = _languages.get(lang)

        if not lang_module:
            lang_module = _languages.get("English")

        self.TITLES = lang_module.TITLES
        self.MENU_OPTIONS = lang_module.MENU_OPTIONS
        self.SUCCESS = lang_module.SUCCESS
        self.WARNINGS = lang_module.WARNINGS
        self.RESULTS = lang_module.RESULTS
        self.LABELS = lang_module.LABELS
        self.BUTTONS = lang_module.BUTTONS
        self.CHART_LABELS = lang_module.CHART_LABELS
        self.set_language(lang)

    def set_language(self, lang):
        lang_module = _languages.get(lang)

        if not lang_module:
            lang_module = _languages.get("English")

        self.TITLES = lang_module.TITLES
        self.MENU_OPTIONS = lang_module.MENU_OPTIONS
        self.SUCCESS = lang_module.SUCCESS
        self.WARNINGS = lang_module.WARNINGS
        self.RESULTS = lang_module.RESULTS
        self.LABELS = lang_module.LABELS
        self.BUTTONS = lang_module.BUTTONS
        self.CHART_LABELS = lang_module.CHART_LABELS

# lang_files = {
#     "pt": ".pt",
#     "en": ".en"
# }
#
# def load_messages(lang):
#     exec(f"from {lang_files[lang]} import ")
#     exec(f"return")