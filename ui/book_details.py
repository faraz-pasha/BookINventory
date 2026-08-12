from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import Qt, Signal

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
            600,
            600
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
            "finished"
            if book.get("is_read")
            else "want_to_read"
        )

        status_text = {
            "want_to_read":
                "📚 Want to Read",

            "currently_reading":
                "📖 Currently Reading",

            "finished":
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

        status.setProperty(
            "status",
            "read" if book["is_read"] else "unread"
        )


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

        info_layout.addStretch()


        top_layout.addLayout(
            info_layout
        )


        main_layout.addLayout(
            top_layout
        )


        # --------------------
        # Notes
        # --------------------

        notes_label = QLabel(
            "Notes"
        )

        notes_label.setObjectName(
            "sectionTitle"
        )


        notes = QTextEdit()

        notes.setText(
            book["notes"]
        )

        notes.setReadOnly(
            True
        )

        notes.setMinimumHeight(
            150
        )


        main_layout.addWidget(
            notes_label
        )

        main_layout.addWidget(
            notes
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