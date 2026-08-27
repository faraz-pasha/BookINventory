from pathlib import Path

from PySide6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QLabel,
)

from PySide6.QtCore import (
    Qt,
    Signal,
)

from PySide6.QtGui import QPixmap

from constants import (
    STATUS_WANT_TO_READ,
    STATUS_CURRENTLY_READING,
    STATUS_FINISHED,
)


class BookCard(QFrame):

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
        # Reading status
        # -------------------

        status_text = {
            STATUS_WANT_TO_READ:
                "📚 Want to Read",

            STATUS_CURRENTLY_READING:
                "📖 Currently Reading",

            STATUS_FINISHED:
                "✓ Finished",
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