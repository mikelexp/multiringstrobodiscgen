import sys
from PySide6.QtWidgets import QApplication
from src.main_window import StroboscopeMultiRingsGenerator

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StroboscopeMultiRingsGenerator()
    window.show()
    sys.exit(app.exec())
