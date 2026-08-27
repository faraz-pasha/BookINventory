from datetime import datetime
from pathlib import Path
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QTextEdit,
    QPushButton,
    QMessageBox,
)

from PySide6.QtGui import QPixmap

from PySide6.QtCore import (
    Qt,
    Signal,
)

from constants import (
    STATUS_WANT_TO_READ,
    STATUS_CURRENTLY_READING,
    STATUS_FINISHED,
)

class BookDetails(QDialog):

    edit_requested = Signal(dict)
    delete_requested = Signal(dict)

    def __init__(self, book):

        super().__init__()

        self.book = book

        self.setWindowTitle(
            book["title"]
        )

        self.resize(
            850,
            650
        )

        self.setObjectName(
            "bookDetails"
        )


        main_layout = QVBoxLayout(self)

        main_layout.setContentsMargins(
            20,
            20,
            20,
            20
        )

        main_layout.setSpacing(
            15
        )


        # --------------------
        # Top section
        # --------------------

        top_layout = QHBoxLayout()

        top_layout.setSpacing(
            20
        )


        # Cover

        cover = QLabel()

        cover.setFixedSize(
            200,
            300
        )

        cover.setAlignment(
            Qt.AlignCenter
        )


        if book["cover"]:

            pixmap = QPixmap(
                book["cover"]
            )

            pixmap = pixmap.scaled(
                200,
                300,
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


        top_layout.addWidget(
            cover
        )


        # Information

        info_layout = QVBoxLayout()

        info_layout.setSpacing(
            8
        )


        title = QLabel(
            book["title"]
        )

        title.setObjectName(
            "detailsTitle"
        )

        title.setWordWrap(
            True
        )


        author = QLabel(
            "Author: " + book["author"]
        )


        genre = QLabel(
            "Genre: " + book["genre"]
        )


        pages = QLabel(
            "Pages: " + str(book["pages"])
        )


        rating = QLabel(
            "Rating: " +
            ("★" * book["rating"])
        )

        reading_status = book.get(
            "reading_status",
            STATUS_FINISHED
            if book.get("is_read")
            else STATUS_WANT_TO_READ
        )

        status_text = {
            STATUS_WANT_TO_READ:
                "📚 Want to Read",

            STATUS_CURRENTLY_READING:
                "📖 Currently Reading",

            STATUS_FINISHED:
                "✅ Finished"
        }

        status = QLabel(
            "Status: " +
            status_text.get(
                reading_status,
                "Want to Read"
            )
        )

        status.setObjectName(
            "detailsStatus"
        )

        self.setProperty(
            "status",
            reading_status
        )

        self.style().unpolish(
            self
        )

        self.style().polish(
            self
        )

        date_added = QLabel(
            "Date Added: "
            + self.format_date(
                book.get("date_added")
            )
        )

        date_read = QLabel()

        if book.get("date_read"):

            date_read.setText(
                "Date Read: "
                + self.format_date(
                    book["date_read"]
                )
            )

        else:

            date_read.hide()


        info_layout.addWidget(
            title
        )

        info_layout.addWidget(
            author
        )

        info_layout.addWidget(
            genre
        )

        info_layout.addWidget(
            pages
        )

        info_layout.addWidget(
            rating
        )

        info_layout.addWidget(
            status
        )

        info_layout.addWidget(
            date_added
        )

        info_layout.addWidget(
            date_read
        )

        info_layout.addStretch()


        top_layout.addLayout(
            info_layout
        )


        main_layout.addLayout(
            top_layout
        )

        # --------------------
        # Description + Notes
        # --------------------

        bottom_layout = QHBoxLayout()

        bottom_layout.setSpacing(
            15
        )

        # --------------------
        # Description
        # --------------------

        description_layout = QVBoxLayout()

        description_label = QLabel(
            "Description"
        )

        description_label.setObjectName(
            "sectionTitle"
        )

        description = QTextEdit()

        description.setText(
            book.get("description")
            or "No description available."
        )

        description.setReadOnly(
            True
        )

        description.setMinimumHeight(
            180
        )

        description_layout.addWidget(
            description_label
        )

        description_layout.addWidget(
            description
        )

        # --------------------
        # Notes
        # --------------------

        notes_layout = QVBoxLayout()

        notes_label = QLabel(
            "Notes"
        )

        notes_label.setObjectName(
            "sectionTitle"
        )

        notes = QTextEdit()

        notes.setText(
            book.get("notes")
            or "No notes."
        )

        notes.setReadOnly(
            True
        )

        notes.setMinimumHeight(
            180
        )

        notes_layout.addWidget(
            notes_label
        )

        notes_layout.addWidget(
            notes
        )

        # --------------------
        # Add both columns
        # --------------------

        bottom_layout.addLayout(
            description_layout,
            1
        )

        bottom_layout.addLayout(
            notes_layout,
            1
        )

        main_layout.addLayout(
            bottom_layout
        )

        # --------------------
        # Buttons
        # --------------------

        buttons = QHBoxLayout()

        edit = QPushButton(
            "✏️ Edit"
        )

        delete = QPushButton(
            "🗑️ Delete"
        )

        close = QPushButton(
            "Close"
        )


        edit.clicked.connect(
            self.edit_book
        )

        delete.clicked.connect(
            self.delete_book
        )

        close.clicked.connect(
            self.close
        )


        buttons.addWidget(
            edit
        )

        buttons.addWidget(
            delete
        )

        buttons.addStretch()

        buttons.addWidget(
            close
        )


        main_layout.addLayout(
            buttons
        )


    def edit_book(self):

        self.edit_requested.emit(
            self.book
        )

        self.close()


    def delete_book(self):

        answer = QMessageBox.question(
            self,
            "Delete Book",
            "Are you sure you want to delete this book?"
        )

        if answer == QMessageBox.Yes:

            self.delete_requested.emit(
                self.book
            )

            self.close()

    def format_date(self, date_string):

        if not date_string:
            return "Unknown"

        try:

            date = datetime.strptime(
                date_string,
                "%Y-%m-%d"
            )

            return date.strftime(
                "%b %d, %Y"
            )

        except ValueError:

            return date_string