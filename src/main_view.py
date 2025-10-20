from PySide6.QtCore import Qt, QEvent
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QMainWindow,
    QPushButton,
    QComboBox
)

class MainView(QMainWindow):

    def setup_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        self.central_widget.setLayout(main_layout)

        self.language_combo = QComboBox()
        main_layout.addWidget(self.language_combo)

        self.button = QPushButton()
        main_layout.addWidget(self.button)

    def retranslate_ui(self):
        self.setWindowTitle(self.tr('pyside6-starter-training'))
        self.button.setText(self.tr('Click Me'))

    def changeEvent(self, event: QEvent) -> None:
        if event.type() == QEvent.LanguageChange:
            self.retranslate_ui()
        super().changeEvent(event)