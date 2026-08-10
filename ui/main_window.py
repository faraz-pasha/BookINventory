from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
from PySide6.QtCore import QSize
from ui.add_book_dialog import AddBookDialog
from ui.book_card import BookCard
from database import (
    add_book,
    get_books,
    update_book,
    delete_book,
    find_books,
    get_genre_counts
)
from ui.book_details import BookDetails


class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(
            "📚 My Library"
        )

        self.resize(1200, 700)

        central_widget = QWidget()

        central_widget.setObjectName(
            "centralWidget"
        )

        self.setCentralWidget(
            central_widget
        )

        main_layout = QHBoxLayout(central_widget)

        # -----------------
        # Sidebar
        # -----------------

        self.sidebar = QTreeWidget()

        self.sidebar.setHeaderHidden(True)

        self.sidebar.itemClicked.connect(
            self.sidebar_clicked
        )
        self.sidebar.setStyleSheet("""

        QTreeWidget {

            font-size:16px;
            padding:10px;

        }

        QTreeWidget::item {

            padding:12px;

        }

        QTreeWidget::item:selected {

            background:#dddddd;

        }

        """)
        self.sidebar.setFixedWidth(
            240
        )

        self.update_shelves()

        self.sidebar.itemClicked.connect(
            self.sidebar_clicked
        )

        main_layout.addWidget(
            self.sidebar
        )

        # -----------------
        # Right side
        # -----------------

        right = QVBoxLayout()

        top_bar = QHBoxLayout()

        # Right side

        right = QVBoxLayout()

        # Top bar
        top_bar = QHBoxLayout()

        self.search_bar = QLineEdit()

        self.search_bar.setPlaceholderText(
            "🔍 Search books..."
        )
        self.sort_box = QComboBox()

        self.sort_box.addItems([
            "Default",
            "Title A-Z",
            "Author A-Z",
            "Rating High-Low",
            "Pages High-Low"
        ])

        self.sort_box.currentTextChanged.connect(
            self.sort_books
        )
        self.search_bar.setClearButtonEnabled(
            True
        )

        self.search_bar.textChanged.connect(
            self.search_books
        )

        button = QPushButton(
            "+ Add Book"
        )

        button.clicked.connect(
            self.add_book
        )

        top_bar.addWidget(
            self.search_bar
        )

        top_bar.addWidget(
            self.sort_box
        )

        top_bar.addWidget(
            button
        )

        right.addLayout(
            top_bar
        )
        self.book_container = QWidget()

        self.book_container.setObjectName(
            "booksArea"
        )
        self.grid = QGridLayout(
            self.book_container
        )
        self.card_width = 200
        self.grid.setContentsMargins(
            20,
            20,
            20,
            20
        )
        self.grid.setSpacing(20)

        self.scroll_books = QScrollArea()

        self.scroll_books.setWidgetResizable(
            True
        )

        self.scroll_books.setWidget(
            self.book_container
        )

        right.addWidget(
            self.scroll_books
        )

        main_layout.addLayout(
            right
        )

        self.current_genre = "All Books"
        self.current_sort = "Default"
        self.load_books()



    def add_book(self):

        dialog = AddBookDialog()


        if dialog.exec():

            add_book(
                dialog.get_data()
            )

            self.update_shelves()
            self.load_books()

    def load_books(self):

        self.display_books(
            get_books()
        )

    def display_books(self, books):
        self.current_books = self.apply_sort(
            books
        )
        books = self.current_books
        # Clear old cards
        while self.grid.count():

            item = self.grid.takeAt(0)

            widget = item.widget()

            if widget:
                widget.deleteLater()

        # Calculate columns dynamically

        available_width = (
            self.scroll_books.viewport().width()
        )

        columns = max(
            1,
            available_width // self.card_width
        )

        row = 0
        col = 0

        for book in books:

            card = BookCard(book)
            card.details_requested.connect(
                self.show_details
            )
            card.edit_requested.connect(
                self.edit_book
            )

            self.grid.addWidget(
                card,
                row,
                col
            )

            col += 1

            if col >= columns:
                col = 0
                row += 1



    def edit_book(self, book):

        dialog = AddBookDialog(book)

        if dialog.exec():
            update_book(
                book["id"],
                dialog.get_data()
            )

            # Refresh shelves after genre changes
            self.update_shelves()

            # Refresh displayed books
            self.load_books()

    def resizeEvent(self, event):

        super().resizeEvent(event)

        if hasattr(self, "current_books"):
            self.display_books(
                self.current_books
            )

    def show_details(self, book):

        dialog = BookDetails(
            book
        )

        dialog.edit_requested.connect(
            self.edit_book
        )

        dialog.delete_requested.connect(
            self.remove_book
        )

        dialog.exec()

    def remove_book(self, book):

        delete_book(
            book["id"]
        )

        self.update_shelves()

        self.load_books()
    def search_books(self, text):

        if text.strip():

            books = find_books(text)

        else:

            books = get_books()

        if self.current_genre != "All Books":
            books = [
                b for b in books
                if b["genre"] == self.current_genre
            ]

        self.display_books(
            self.apply_sort(books)
        )

    def update_shelves(self):

        self.sidebar.clear()

        books = get_books()

        sections = [
            ("📚 All Books", "all"),
            ("✅ Read", "read"),
            ("📖 Unread", "unread")
        ]

        for name, status in sections:

            parent = QTreeWidgetItem(
                [name]
            )

            self.sidebar.addTopLevelItem(
                parent
            )

            if status == "read":

                filtered = [
                    b for b in books
                    if b["is_read"]
                ]

            elif status == "unread":

                filtered = [
                    b for b in books
                    if not b["is_read"]
                ]

            else:

                filtered = books

            # All genres option

            all_item = QTreeWidgetItem(
                [
                    f"📚 All Genres ({len(filtered)})"
                ]
            )

            all_item.setData(
                0,
                Qt.UserRole,
                (status, "all")
            )

            parent.addChild(
                all_item
            )

            genres = {}

            for book in filtered:
                genre = book["genre"]

                genres[genre] = (
                        genres.get(genre, 0) + 1
                )

            for genre, count in sorted(
                    genres.items()
            ):
                item = QTreeWidgetItem(
                    [
                        f"📖 {genre} ({count})"
                    ]
                )

                item.setData(
                    0,
                    Qt.UserRole,
                    (status, genre)
                )

                parent.addChild(
                    item
                )

            parent.setExpanded(
                True
            )

    def sidebar_clicked(self, item, column):

        data = item.data(
            0,
            Qt.UserRole
        )

        books = get_books()

        # Top-level clicked
        if data is None:

            text = item.text(0)

            if "All Books" in text:

                self.display_books(
                    books
                )

            elif "Read" in text:

                books = [
                    b for b in books
                    if b["is_read"]
                ]

                self.display_books(
                    books
                )

            elif "Unread" in text:

                books = [
                    b for b in books
                    if not b["is_read"]
                ]

                self.display_books(
                    books
                )

            return

        # Genre clicked
        status, genre = data

        if status == "read":

            books = [
                b for b in books
                if b["is_read"]
            ]

        elif status == "unread":

            books = [
                b for b in books
                if not b["is_read"]
            ]

        if genre != "all":
            books = [
                b for b in books
                if b["genre"] == genre
            ]

        self.display_books(
            books
        )

    def sort_books(self, option):

        self.current_sort = option

        books = self.current_books.copy()

        books = self.apply_sort(
            books
        )

        self.display_books(
            books
        )

    def apply_sort(self, books):

        if self.current_sort == "Title A-Z":

            books.sort(
                key=lambda x: x["title"].lower()
            )


        elif self.current_sort == "Author A-Z":

            books.sort(
                key=lambda x: (
                        x["author"] or ""
                ).lower()
            )


        elif self.current_sort == "Rating High-Low":

            books.sort(
                key=lambda x: x["rating"],
                reverse=True
            )


        elif self.current_sort == "Pages High-Low":

            books.sort(
                key=lambda x: x["pages"] or 0,
                reverse=True
            )

        return books