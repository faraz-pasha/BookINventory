from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QMessageBox,
)


class BookLookupDialog(QDialog):

    def __init__(
        self,
        results,
        parent=None,
    ):

        super().__init__(
            parent
        )

        self.setObjectName(
            "bookLookupDialog"
        )

        self.setWindowTitle(
            "Select Book"
        )

        self.resize(
            500,
            500
        )

        self.results = results
        self.selected_book = None

        layout = QVBoxLayout(
            self
        )

        title = QLabel(
            "Select the correct book"
        )

        title.setObjectName(
            "lookupTitle"
        )

        layout.addWidget(
            title
        )

        self.result_list = QListWidget()

        self.result_list.setObjectName(
            "lookupResults"
        )

        layout.addWidget(
            self.result_list
        )

        self.populate_results()

        select_button = QPushButton(
            "Use This Book"
        )

        select_button.clicked.connect(
            self.select_book
        )

        layout.addWidget(
            select_button
        )

        self.result_list.itemDoubleClicked.connect(
            self.select_book
        )

    def populate_results(
        self
    ):

        for index, book in enumerate(
            self.results
        ):

            title = (
                book.get("title")
                or "Unknown Title"
            )

            author = (
                book.get("author")
                or "Unknown Author"
            )

            published_date = (
                book.get("published_date")
                or "Unknown date"
            )

            pages = (
                book.get("pages")
                or 0
            )

            isbn = (
                book.get("isbn")
                or "No ISBN"
            )

            text = (
                f"{title}\n"
                f"{author}\n"
                f"{published_date} | "
                f"{pages} pages | "
                f"{isbn}"
            )

            item = QListWidgetItem(
                text
            )

            item.setData(
                Qt.UserRole,
                index
            )

            self.result_list.addItem(
                item
            )

    def select_book(
        self,
        item=None
    ):

        if item is None:

            item = (
                self.result_list
                .currentItem()
            )

        if item is None:

            QMessageBox.warning(
                self,
                "No Book Selected",
                "Please select a book."
            )

            return

        index = item.data(
            Qt.UserRole
        )

        self.selected_book = (
            self.results[
                index
            ]
        )

        self.accept()

    def get_selected_book(
        self
    ):

        return self.selected_book