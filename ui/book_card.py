from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *


class BookCard(QFrame):

    edit_requested = Signal(dict)
    details_requested = Signal(dict)

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
            "finished"
            if book.get("is_read")
            else "want_to_read"
        )

        # -------------------
        # Card styling property
        # -------------------

        self.setProperty(
            "status",
            self.reading_status
        )

        self.style().unpolish(self)
        self.style().polish(self)

        # -------------------
        # Card size
        # -------------------

        self.setFixedSize(
            200,
            450
        )

        layout = QVBoxLayout(self)

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

        if book["cover"]:

            pixmap = QPixmap(
                book["cover"]
            )

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
            Qt.AlignCenter
        )

        title.setWordWrap(
            True
        )

        title.setMinimumHeight(
            45
        )

        title.setMaximumHeight(
            65
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
        # Rating
        # -------------------

        rating = book.get(
            "rating",
            0
        ) or 0

        if rating > 0:

            stars = QLabel(
                "★" * rating
            )

        else:

            stars = QLabel(
                "No Rating"
            )

        stars.setAlignment(
            Qt.AlignCenter
        )

        layout.addWidget(
            stars
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

        # -------------------
        # Reading Status
        # -------------------

        status_text = {

            "want_to_read":
                "📚 Want to Read",

            "currently_reading":
                "📖 Currently Reading",

            "finished":
                "✓ Finished"
        }

        status = QLabel(
            status_text.get(
                self.reading_status,
                "📚 Want to Read"
            )
        )

        status.setAlignment(
            Qt.AlignCenter
        )

        layout.addWidget(
            status
        )

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