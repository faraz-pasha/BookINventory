import sys

from PySide6.QtWidgets import QApplication

from ui.main_window import MainWindow

from database import get_connection


get_connection()


app = QApplication(sys.argv)


with open("style.qss","r") as file:

    app.setStyleSheet(
        file.read()
    )


window = MainWindow()

window.show()


sys.exit(
    app.exec()
)
