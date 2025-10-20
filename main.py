import sys

from PySide6.QtWidgets import QApplication

from src.main_view_model import MainViewModel

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainViewModel(app)
    window.show()
    sys.exit(app.exec())