from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtCore import Qt, Signal


class BookCard(QFrame):

    edit_requested = Signal(dict)
    details_requested = Signal(dict)

    def __init__(self, book):

        super().__init__()

        self.book = book

        self.setObjectName(
            "bookCard"
        )

        # Read/unread styling property
        self.setProperty(
            "status",
            "read" if book["is_read"] else "unread"
        )

        self.style().unpolish(self)
        self.style().polish(self)

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

        stars = QLabel(
            "★" * book["rating"]
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
        # Status
        # -------------------

        status = QLabel(
            "✓ Read"
            if book["is_read"]
            else
            "Unread"
        )

        status.setAlignment(
            Qt.AlignCenter
        )

        layout.addWidget(
            status
        )


    def mouseDoubleClickEvent(self, event):

        self.details_requested.emit(
            self.book
        )