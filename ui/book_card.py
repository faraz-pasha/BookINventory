from pathlib import Path

from PySide6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QMenu,
)

from PySide6.QtCore import (
    Qt,
    Signal,
)

from PySide6.QtGui import (
    QPixmap,
    QAction,
)

from constants import (
    STATUS_WANT_TO_READ,
    STATUS_CURRENTLY_READING,
    STATUS_FINISHED,
)


class BookCard(QFrame):

    details_requested = Signal(dict)
    status_change_requested = Signal(dict, str)
    rating_change_requested = Signal(dict, int)

    def __init__(self, book):

        super().__init__()

        self.book = book

        self.setObjectName(
            "bookCard"
        )

        # -------------------
        # Reading status
        # -------------------

        self.reading_status = book.get(
            "reading_status",
            STATUS_FINISHED
            if book.get("is_read")
            else STATUS_WANT_TO_READ
        )

        # -------------------
        # Card styling property
        # -------------------

        self.setProperty(
            "status",
            self.reading_status
        )

        self.style().unpolish(
            self
        )

        self.style().polish(
            self
        )

        # -------------------
        # Card size
        # -------------------

        self.setFixedSize(
            200,
            450
        )

        layout = QVBoxLayout(
            self
        )

        layout.setContentsMargins(
            10,
            10,
            10,
            10
        )

        layout.setSpacing(
            6
        )

        layout.setAlignment(
            Qt.AlignTop
        )

        # -------------------
        # Cover
        # -------------------

        cover = QLabel()

        cover.setFixedSize(
            150,
            220
        )

        cover.setAlignment(
            Qt.AlignCenter
        )

        cover_path = book.get(
            "cover"
        )

        if cover_path:

            path = Path(
                cover_path
            )

            if path.exists():

                pixmap = QPixmap(
                    str(path)
                )

                if not pixmap.isNull():

                    pixmap = pixmap.scaled(
                        150,
                        220,
                        Qt.KeepAspectRatio,
                        Qt.SmoothTransformation
                    )

                    cover.setPixmap(
                        pixmap
                    )

                else:

                    cover.setText(
                        "No Cover"
                    )

            else:

                cover.setText(
                    "No Cover"
                )

        else:

            cover.setText(
                "No Cover"
            )

        layout.addWidget(
            cover,
            alignment=Qt.AlignTop | Qt.AlignHCenter
        )

        # -------------------
        # Title
        # -------------------

        title = QLabel(
            book["title"]
        )

        title.setObjectName(
            "bookTitle"
        )

        title.setAlignment(
            Qt.AlignTop
            | Qt.AlignHCenter
        )

        title.setWordWrap(
            True
        )

        title.setFixedHeight(
            75
        )

        layout.addWidget(
            title
        )

        # -------------------
        # Author
        # -------------------

        author = QLabel(
            book["author"]
        )

        author.setWordWrap(
            True
        )

        author.setAlignment(
            Qt.AlignCenter
        )

        layout.addWidget(
            author
        )
        # -------------------
        # Genre
        # -------------------

        genre = QLabel(
            book["genre"]
        )

        genre.setAlignment(
            Qt.AlignCenter
        )

        layout.addWidget(
            genre
        )

        layout.addSpacing(
            4
        )




        # -------------------
        # Rating
        # -------------------

        self.rating = book.get(
            "rating",
            0
        ) or 0

        rating_text = (
            "★" * self.rating
            if self.rating > 0
            else "No Rating"
        )


        self.rating_button = QPushButton(
            rating_text
        )

        self.rating_button.setObjectName(
            "ratingButton"
        )

        self.rating_button.setCursor(
            Qt.PointingHandCursor
        )

        self.rating_button.clicked.connect(
            self.show_rating_menu
        )
        self.rating_button.setFixedHeight(24)

        layout.addWidget(
            self.rating_button,
            alignment=Qt.AlignHCenter
        )

        layout.addSpacing(
            4
        )

        # -------------------
        # Reading status
        # -------------------

        self.status_text = {
            STATUS_WANT_TO_READ:
                "📚 Want to Read",

            STATUS_CURRENTLY_READING:
                "Currently Reading",

            STATUS_FINISHED:
                "✓ Finished",
        }

        self.status_button = QPushButton(
            self.status_text.get(
                self.reading_status,
                "📚 Want to Read"
            )
        )

        self.status_button.setObjectName(
            "statusButton"
        )

        self.status_button.setCursor(
            Qt.PointingHandCursor
        )

        self.status_button.clicked.connect(
            self.show_status_menu
        )
        self.status_button.setFixedHeight(24)
        layout.addWidget(
            self.status_button,
            alignment=Qt.AlignHCenter
        )

    # -------------------
    # Status menu
    # -------------------

    def show_status_menu(
        self
    ):

        menu = QMenu(
            self
        )

        statuses = [
            (
                "📚 Want to Read",
                STATUS_WANT_TO_READ
            ),
            (
                "📖 Currently Reading",
                STATUS_CURRENTLY_READING
            ),
            (
                "✓ Finished",
                STATUS_FINISHED
            ),
        ]

        for text, status_value in statuses:

            action = QAction(
                text,
                menu
            )

            action.setCheckable(
                True
            )

            action.setChecked(
                status_value
                == self.reading_status
            )

            action.triggered.connect(
                lambda checked=False,
                value=status_value:
                self.request_status_change(
                    value
                )
            )

            menu.addAction(
                action
            )

        menu.exec(
            self.status_button.mapToGlobal(
                self.status_button.rect().bottomLeft()
            )
        )

    # -------------------
    # Request status change
    # -------------------

    def request_status_change(
        self,
        new_status
    ):

        if new_status == self.reading_status:
            return

        self.status_change_requested.emit(
            self.book,
            new_status
        )

    # -------------------
    # Book details
    # -------------------

    def mouseDoubleClickEvent(
        self,
        event
    ):

        self.details_requested.emit(
            self.book
        )

        super().mouseDoubleClickEvent(
            event
        )

    # -------------------
    # Rating menu
    # -------------------

    def show_rating_menu(
            self
    ):

        menu = QMenu(
            self
        )

        ratings = [
            ("No Rating", 0),
            ("★", 1),
            ("★★", 2),
            ("★★★", 3),
            ("★★★★", 4),
            ("★★★★★", 5),
        ]

        for text, rating_value in ratings:
            action = QAction(
                text,
                menu
            )

            action.setCheckable(
                True
            )

            action.setChecked(
                rating_value
                == self.rating
            )

            action.triggered.connect(
                lambda checked=False,
                       value=rating_value:
                self.request_rating_change(
                    value
                )
            )

            menu.addAction(
                action
            )

        menu.exec(
            self.rating_button.mapToGlobal(
                self.rating_button.rect().bottomLeft()
            )
        )

    def request_rating_change(
            self,
            new_rating
    ):

        if new_rating == self.rating:
            return

        self.rating_change_requested.emit(
            self.book,
            new_rating
        )