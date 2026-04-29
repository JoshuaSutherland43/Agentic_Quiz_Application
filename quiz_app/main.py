import sys
from gui import QuizApp

if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = QuizApp()
    window.show()
    sys.exit(app.exec_())
