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

    get_genre_counts
)
from PySide6.QtCore import QTimer
from ui.book_details import BookDetails
from ui.statistics_page import StatisticsPage
from ui.suggestion_page import SuggestionPage

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



        main_layout.addWidget(
            self.sidebar
        )

        # -----------------
        # Right side
        # -----------------


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
            "Title",
            "Author",
            "Rating",
            "Pages",
            "Date Added",
            "Date Read"
        ])


        self.sort_box.currentTextChanged.connect(
            self.sort_books
        )

        self.sort_direction = "asc"

        self.sort_direction_button = QPushButton(
            "↑"
        )

        self.sort_direction_button.setFixedWidth(
            40
        )

        self.sort_direction_button.setToolTip(
            "Change sort direction"
        )

        self.sort_direction_button.clicked.connect(
            self.toggle_sort_direction
        )

        self.search_bar.setClearButtonEnabled(
            True
        )

        self.search_bar.textChanged.connect(
            self.search_books
        )

        sort_label = QLabel(
            "Sort by:"
        )

        button = QPushButton(
            "+ Add Book"
        )


        statistics_button = QPushButton(
            "📊 Statistics"
        )

        suggestion_button = QPushButton(
            "🎲 Suggestions"
        )
        suggestion_button.clicked.connect(
            self.show_suggestions
        )
        statistics_button.clicked.connect(
            self.show_statistics
        )

        books_button = QPushButton(
            "📚 Books"
        )

        books_button.clicked.connect(
            self.show_books
        )

        button.clicked.connect(
            self.add_book
        )

        top_bar.addWidget(
            self.search_bar
        )

        top_bar.addWidget(
            sort_label
        )

        top_bar.addWidget(
            self.sort_box
        )

        top_bar.addWidget(
            self.sort_direction_button
        )

        top_bar.addWidget(
            books_button
        )

        top_bar.addWidget(
            statistics_button
        )

        top_bar.addWidget(
            suggestion_button
        )

        top_bar.addWidget(
            button
        )

        right.addLayout(
            top_bar
        )
        self.statistics_page = StatisticsPage()

        self.statistics_page.hide()

        self.suggestion_page = SuggestionPage()

        self.suggestion_page.hide()

        self.suggestion_page.details_requested.connect(
            self.show_details
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
        self.grid.setSpacing(10)

        self.scroll_books = QScrollArea()

        self.scroll_books.setWidgetResizable(
            True
        )

        self.scroll_books.setWidget(
            self.book_container
        )
        right.addWidget(
            self.statistics_page
        )
        right.addWidget(
            self.suggestion_page
        )
        right.addWidget(
            self.scroll_books
        )

        main_layout.addLayout(
            right
        )

        self.current_status = "all"
        self.current_genre = "all"
        self.current_search = ""
        self.current_sort = "Default"

        QTimer.singleShot(
            0,
            self.load_books
        )




    def add_book(self):

        dialog = AddBookDialog()


        if dialog.exec():

            add_book(
                dialog.get_data()
            )

            self.update_shelves()
            self.load_books()

    def load_books(self):

        books = self.get_current_filter_books()

        self.display_books(
            books
        )

    def display_books(self, books):

        books = self.apply_sort(
            books
        )

        self.current_books = books
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
            available_width // (
                    self.card_width + 10
            )
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

        if hasattr(
                self,
                "scroll_books"
        ):
            self.load_books()

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

        self.current_search = text

        self.load_books()

    def update_shelves(self):

        self.sidebar.clear()

        books = get_books()

        sections = [
            ("📚 All Books", "all"),
            ("📚 Want to Read", "want_to_read"),
            ("📖 Currently Reading", "currently_reading"),
            ("✅ Finished", "finished")
        ]

        for name, status in sections:

            parent = QTreeWidgetItem(
                [name]
            )

            self.sidebar.addTopLevelItem(
                parent
            )

            # -------------------------
            # Filter by reading status
            # -------------------------

            if status == "want_to_read":

                filtered = [
                    book
                    for book in books
                    if book["reading_status"]
                       == "want_to_read"
                ]

            elif status == "currently_reading":

                filtered = [
                    book
                    for book in books
                    if book["reading_status"]
                       == "currently_reading"
                ]

            elif status == "finished":

                filtered = [
                    book
                    for book in books
                    if book["reading_status"]
                       == "finished"
                ]

            else:

                filtered = books

            # -------------------------
            # All Genres
            # -------------------------

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

            # -------------------------
            # Genre counts
            # -------------------------

            genres = {}

            for book in filtered:

                genre = book["genre"]

                if genre:
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

    def sidebar_clicked(
            self,
            item,
            column
    ):

        data = item.data(
            0,
            Qt.UserRole
        )

        if data is None:
            return

        status, genre = data

        self.current_status = status

        self.current_genre = genre

        # Update the books
        self.load_books()

    def sort_books(self, option):

        self.current_sort = option

        if option in [
            "Rating",
            "Pages",
            "Date Added",
            "Date Read"
        ]:

            self.sort_direction = "desc"

            self.sort_direction_button.setText(
                "↓"
            )

        else:

            self.sort_direction = "asc"

            self.sort_direction_button.setText(
                "↑"
            )

        self.load_books()

    def apply_sort(self, books):

        reverse = (
                self.sort_direction
                == "desc"
        )

        if self.current_sort == "Title":

            books.sort(
                key=lambda x: (
                        x["title"] or ""
                ).lower(),
                reverse=reverse
            )


        elif self.current_sort == "Author":

            books.sort(
                key=lambda x: (
                        x["author"] or ""
                ).lower(),
                reverse=reverse
            )


        elif self.current_sort == "Rating":

            books.sort(
                key=lambda x: (
                        x["rating"] or 0
                ),
                reverse=reverse
            )


        elif self.current_sort == "Pages":

            books.sort(
                key=lambda x: (
                        x["pages"] or 0
                ),
                reverse=reverse
            )


        elif self.current_sort == "Date Added":

            books.sort(
                key=lambda x: (
                        x.get("date_added")
                        or ""
                ),
                reverse=reverse
            )


        elif self.current_sort == "Date Read":

            books.sort(
                key=lambda x: (
                        x.get("date_read")
                        or ""
                ),
                reverse=reverse
            )

        return books

    def show_books(self):

        self.statistics_page.hide()

        self.suggestion_page.hide()

        self.scroll_books.show()

        self.search_bar.show()

        self.sort_box.show()

    def show_statistics(self):

        self.scroll_books.hide()

        self.suggestion_page.hide()

        self.statistics_page.show()

        self.search_bar.hide()

        self.sort_box.hide()

        books = self.get_current_filter_books()

        self.statistics_page.update_statistics(
            books,
            self.current_statistics_title()
        )

    def show_suggestions(self):

        self.scroll_books.hide()

        self.statistics_page.hide()

        self.suggestion_page.show()

        self.search_bar.hide()

        self.sort_box.hide()

        # Refresh genres in case a new
        # genre was recently added.

        self.suggestion_page.load_genres()

    def current_statistics_title(self):

        status_names = {
            "want_to_read":
                "Want to Read",

            "currently_reading":
                "Currently Reading",

            "finished":
                "Finished"
        }

        status_name = status_names.get(
            self.current_status
        )

        if status_name:

            if self.current_genre != "all":
                return (
                    f"{status_name} → "
                    f"{self.current_genre} "
                    "Statistics"
                )

            return (
                f"{status_name} "
                "Statistics"
            )

        if self.current_genre != "all":
            return (
                f"{self.current_genre} "
                "Statistics"
            )

        return "Library Statistics"
    def get_current_filter_books(self):

        books = get_books()

        # -------------------------
        # Reading status
        # -------------------------

        if self.current_status != "all":
            books = [
                book
                for book in books
                if book["reading_status"]
                   == self.current_status
            ]

        # -------------------------
        # Genre
        # -------------------------

        if self.current_genre != "all":
            books = [
                book
                for book in books
                if book["genre"]
                   == self.current_genre
            ]

        # -------------------------
        # Search
        # -------------------------

        if self.current_search:
            search_text = (
                self.current_search
                .strip()
                .lower()
            )

            books = [
                book
                for book in books
                if (
                        search_text in (
                        book["title"] or ""
                ).lower()

                        or

                        search_text in (
                                book["author"] or ""
                        ).lower()

                        or

                        search_text in (
                                book["genre"] or ""
                        ).lower()

                        or

                        search_text in (
                                book["notes"] or ""
                        ).lower()
                )
            ]

        return books

    def toggle_sort_direction(self):

        if self.sort_direction == "asc":

            self.sort_direction = "desc"

            self.sort_direction_button.setText(
                "↓"
            )

        else:

            self.sort_direction = "asc"

            self.sort_direction_button.setText(
                "↑"
            )

        self.load_books()