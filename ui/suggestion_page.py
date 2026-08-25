import random

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QSpinBox,
    QPushButton,
    QFrame
)

from PySide6.QtCore import (
    Qt,
    Signal
)

from ui.book_card import BookCard
from database import get_books

from constants import (
    STATUS_WANT_TO_READ,
)
class SuggestionPage(QWidget):

    details_requested = Signal(dict)

    def __init__(self):

        super().__init__()

        self.setObjectName(
            "suggestionPage"
        )

        self.current_matches = []
        self.previous_suggestions = []

        # -------------------------
        # Main layout
        # -------------------------

        main_layout = QVBoxLayout(
            self
        )

        main_layout.setContentsMargins(
            30,
            30,
            30,
            30
        )

        main_layout.setSpacing(
            20
        )

        # -------------------------
        # Top content
        # -------------------------

        top_content = QWidget()

        top_layout = QVBoxLayout(
            top_content
        )

        top_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        top_layout.setSpacing(
            15
        )

        main_layout.addWidget(
            top_content,
            alignment=Qt.AlignLeft
        )

        # -------------------------
        # Title
        # -------------------------

        title = QLabel(
            "🎲 Book Suggestions"
        )

        title.setObjectName(
            "suggestionTitle"
        )

        title.setAlignment(
            Qt.AlignLeft
        )

        top_layout.addWidget(
            title
        )

        # -------------------------
        # Description
        # -------------------------

        description = QLabel(
            "Choose one or more genres and a maximum "
            "page count. Suggestions are selected only "
            "from your Want to Read books."
        )

        description.setWordWrap(
            True
        )

        description.setAlignment(
            Qt.AlignLeft
        )

        top_layout.addWidget(
            description
        )

        # -------------------------
        # Filters
        # -------------------------

        filters = QHBoxLayout()

        filters.setContentsMargins(
            0,
            0,
            0,
            0
        )

        filters.setSpacing(
            20
        )

        filters.setAlignment(
            Qt.AlignLeft | Qt.AlignTop
        )

        # Genre section

        genre_section = QVBoxLayout()

        genre_section.setContentsMargins(
            0,
            0,
            0,
            0
        )

        genre_section.setSpacing(
            6
        )

        genre_label = QLabel(
            "Genres"
        )

        self.genre_list = QListWidget()

        self.genre_list.setFixedWidth(
            220
        )

        self.genre_list.setMaximumHeight(
            150
        )

        genre_section.addWidget(
            genre_label
        )

        genre_section.addWidget(
            self.genre_list
        )

        filters.addLayout(
            genre_section
        )

        # Maximum pages section

        pages_section = QVBoxLayout()

        pages_section.setContentsMargins(
            0,
            0,
            0,
            0
        )

        pages_section.setSpacing(
            6
        )

        pages_label = QLabel(
            "Maximum Pages"
        )

        self.max_pages = QSpinBox()

        self.max_pages.setRange(
            1,
            10000
        )

        self.max_pages.setValue(
            500
        )

        self.max_pages.setFixedWidth(
            150
        )

        pages_section.addWidget(
            pages_label
        )

        pages_section.addWidget(
            self.max_pages
        )

        pages_section.addStretch()

        filters.addLayout(
            pages_section
        )

        # Suggest button section

        button_section = QVBoxLayout()

        button_section.setContentsMargins(
            0,
            0,
            0,
            0
        )

        button_section.setSpacing(
            6
        )

        button_label = QLabel(
            " "
        )

        self.suggest_button = QPushButton(
            "🎲 Suggest Books"
        )

        self.suggest_button.setFixedWidth(
            150
        )

        self.suggest_button.clicked.connect(
            self.find_suggestions
        )

        button_section.addWidget(
            button_label
        )

        button_section.addWidget(
            self.suggest_button
        )

        button_section.addStretch()

        filters.addLayout(
            button_section
        )

        filters.addStretch()

        top_layout.addLayout(
            filters
        )

        # -------------------------
        # Message
        # -------------------------

        self.message = QLabel(
            "Select at least one genre."
        )

        self.message.setObjectName(
            "suggestionMessage"
        )

        self.message.setAlignment(
            Qt.AlignLeft
        )

        top_layout.addWidget(
            self.message
        )

        # -------------------------
        # Results
        # -------------------------

        self.results_frame = QFrame()

        self.results_frame.setObjectName(
            "suggestionResults"
        )

        self.results_layout = QHBoxLayout(
            self.results_frame
        )

        self.results_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        self.results_layout.setSpacing(
            20
        )

        self.results_layout.setAlignment(
            Qt.AlignLeft | Qt.AlignTop
        )

        main_layout.addWidget(
            self.results_frame,
            alignment=Qt.AlignLeft
        )

        main_layout.addStretch()

        self.load_genres()

    def load_genres(self):

        selected_genres = set(
            self.get_selected_genres()
        )

        self.genre_list.clear()

        books = get_books()

        genres = sorted({
            book["genre"]
            for book in books
            if (
                book.get("genre")
                and
                book.get("reading_status")
                == STATUS_WANT_TO_READ
            )
        })

        for genre in genres:

            item = QListWidgetItem(
                genre
            )

            item.setFlags(
                item.flags()
                | Qt.ItemIsUserCheckable
            )

            item.setCheckState(
                Qt.Checked
                if genre in selected_genres
                else Qt.Unchecked
            )

            self.genre_list.addItem(
                item
            )


    def get_selected_genres(self):

        genres = []

        for index in range(
            self.genre_list.count()
        ):

            item = self.genre_list.item(
                index
            )

            if item.checkState() == Qt.Checked:

                genres.append(
                    item.text()
                )

        return genres


    def get_matching_books(self):

        selected_genres = (
            self.get_selected_genres()
        )

        if not selected_genres:

            return []

        max_pages = (
            self.max_pages.value()
        )

        books = get_books()

        return [
            book
            for book in books
            if (
                book.get("reading_status")
                == "want_to_read"

                and
                book.get("genre")
                in selected_genres

                and
                (book.get("pages") or 0) > 0

                and
                (book.get("pages") or 0)
                <= max_pages
            )
        ]


    def find_suggestions(self):

        selected_genres = (
            self.get_selected_genres()
        )

        if not selected_genres:

            self.clear_results()

            self.message.setText(
                "Please select at least one genre."
            )

            return

        new_matches = (
            self.get_matching_books()
        )

        new_ids = {
            book["id"]
            for book in new_matches
        }

        old_ids = {
            book["id"]
            for book in self.current_matches
        }

        # Reset repeat history if
        # the criteria changed
        if new_ids != old_ids:

            self.previous_suggestions = []

        self.current_matches = (
            new_matches
        )

        self.show_random_books()


    def show_random_books(self):

        self.clear_results()

        if not self.current_matches:

            self.message.setText(
                "No Want to Read books match "
                "those criteria."
            )

            return

        count = min(
            3,
            len(self.current_matches)
        )

        previous_ids = {
            book["id"]
            for book
            in self.previous_suggestions
        }

        alternatives = [
            book
            for book in self.current_matches
            if book["id"]
            not in previous_ids
        ]

        if len(alternatives) >= count:

            suggestions = random.sample(
                alternatives,
                count
            )

        else:

            suggestions = random.sample(
                self.current_matches,
                count
            )

        self.previous_suggestions = (
            suggestions
        )

        self.message.setText(
            f"Found {len(self.current_matches)} "
            f"matching Want to Read "
            f"book{'s' if len(self.current_matches) != 1 else ''}."
        )

        for book in suggestions:

            card = BookCard(
                book
            )

            card.details_requested.connect(
                self.details_requested.emit
            )

            self.results_layout.addWidget(
                card
            )


    def clear_results(self):

        while self.results_layout.count():

            item = self.results_layout.takeAt(
                0
            )

            widget = item.widget()

            if widget:

                widget.deleteLater()