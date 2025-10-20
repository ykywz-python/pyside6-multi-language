import os

from PySide6.QtCore import QTranslator, QCoreApplication
from src.main_view import MainView


class MainViewModel(MainView):

    def __init__(self, app):
        super().__init__()
        self.app = app
        self.translator = QTranslator()
        self.languages = {
            "English": "en",
            "Indonesia": "id",
            "Français": "fr",
            "Espanole": "es",
            "Português": "pt"
        }

        # initial windows
        self.resize(300, 300)

        self.init_ui()

    def init_ui(self):
        self.setup_ui()
        self.setup_language_switcher()
        self.retranslate_ui()

        # signal
        self.button.clicked.connect(self.on_button_clicked)

    def setup_language_switcher(self):
        """Populates the combo box and connects its signal."""
        self.language_combo.addItems(self.languages.keys())
        self.language_combo.currentTextChanged.connect(self.on_language_change)

    def on_language_change(self, language_name: str):
        lang_code = self.languages.get(language_name, 'en')
        self.load_language(lang_code)

    def on_button_clicked(self):
        print('button clicked')

    def load_language(self, lang):
        """
        Loads a new language translation.
        If the language code is 'en' (default), it removes the current translator,
        reverting the application to its original language.
        """
        # Always remove the current translator. If we're switching to the default
        # language, we don't need to install a new one.
        self.app.removeTranslator(self.translator)

        # If the target language is the default, we are done.
        if lang != 'en':
            translation_file = os.path.join(os.path.dirname(__file__), 'translations', f'app_{lang}.qm')
            print(f"Loading translation file: {translation_file}")
            if self.translator.load(translation_file):
                self.app.installTranslator(self.translator)
            else:
                print(f"Error: Could not load translation for '{lang}'")