import shutil
from pathlib import Path

from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QComboBox,
    QSpinBox,
    QDateEdit,
    QTextEdit,
    QPushButton,
    QFileDialog,
    QMessageBox,
)

from PySide6.QtCore import QDate
from uuid import uuid4

from constants import (
    STATUS_WANT_TO_READ,
    STATUS_CURRENTLY_READING,
    STATUS_FINISHED,
)



class AddBookDialog(QDialog):

    def __init__(self, book=None):

        super().__init__()

        self.setObjectName(
            "addBookDialog"
        )

        self.book = book

        self.setWindowTitle(
            "Edit Book"
            if book
            else "Add Book"
        )

        self.resize(
            400,
            500
        )

        layout = QVBoxLayout(
            self
        )

        # -------------------------
        # Title / Author
        # -------------------------

        self.title = QLineEdit()
        self.author = QLineEdit()

        # -------------------------
        # Genre
        # -------------------------

        self.genre = QComboBox()

        self.genre.addItems([
            "Fantasy",
            "Fiction",
            "Romance",
            "Mystery",
            "History",
            "Art",
            "Philosophy",
            "Other",
        ])

        self.genre.currentTextChanged.connect(
            self.genre_changed
        )

        self.custom_genre = QLineEdit()

        self.custom_genre.setPlaceholderText(
            "Enter custom genre"
        )

        self.custom_genre.hide()

        # -------------------------
        # Rating / Pages
        # -------------------------

        self.rating = QSpinBox()

        self.rating.setRange(
            0,
            5
        )

        self.pages = QSpinBox()

        self.pages.setRange(
            0,
            10000
        )

        self.pages.setValue(
            100
        )

        # -------------------------
        # Cover
        # -------------------------

        self.cover = QLineEdit()

        browse = QPushButton(
            "Choose Cover"
        )

        browse.clicked.connect(
            self.select_cover
        )

        # -------------------------
        # Reading status
        # -------------------------

        self.reading_status = QComboBox()

        self.reading_status.addItems([
            "Want to Read",
            "Currently Reading",
            "Finished",
        ])

        self.reading_status.currentTextChanged.connect(
            self.reading_status_changed
        )

        # -------------------------
        # Date read
        # -------------------------

        self.date_read_label = QLabel(
            "Date Read"
        )

        self.date_read = QDateEdit()

        self.date_read.setCalendarPopup(
            True
        )

        self.date_read.calendarWidget().setObjectName(
            "dateCalendar"
        )

        self.date_read.setDisplayFormat(
            "MMM d, yyyy"
        )

        self.date_read.setDate(
            QDate.currentDate()
        )

        self.date_read_label.hide()
        self.date_read.hide()

        # -------------------------
        # Notes
        # -------------------------

        self.notes = QTextEdit()

        # -------------------------
        # Layout
        # -------------------------

        layout.addWidget(
            QLabel("Title")
        )

        layout.addWidget(
            self.title
        )

        layout.addWidget(
            QLabel("Author")
        )

        layout.addWidget(
            self.author
        )

        layout.addWidget(
            QLabel("Genre")
        )

        layout.addWidget(
            self.genre
        )

        layout.addWidget(
            self.custom_genre
        )

        layout.addWidget(
            QLabel("Rating")
        )

        layout.addWidget(
            self.rating
        )

        layout.addWidget(
            QLabel("Pages")
        )

        layout.addWidget(
            self.pages
        )

        layout.addWidget(
            self.cover
        )

        layout.addWidget(
            browse
        )

        layout.addWidget(
            QLabel("Reading Status")
        )

        layout.addWidget(
            self.reading_status
        )

        layout.addWidget(
            self.date_read_label
        )

        layout.addWidget(
            self.date_read
        )

        layout.addWidget(
            QLabel("Notes")
        )

        layout.addWidget(
            self.notes
        )

        save = QPushButton(
            "Save"
        )

        save.clicked.connect(
            self.save_book
        )

        layout.addWidget(
            save
        )

        if book:
            self.load_book(
                book
            )

    # =====================================================
    # Load existing book
    # =====================================================

    def load_book(
        self,
        book
    ):

        self.title.setText(
            book["title"] or ""
        )

        self.author.setText(
            book["author"] or ""
        )

        self.pages.setValue(
            book["pages"] or 0
        )

        # -------------------------
        # Genre
        # -------------------------

        genre = (
            book["genre"]
            or ""
        )

        index = self.genre.findText(
            genre
        )

        if index >= 0:

            self.genre.setCurrentIndex(
                index
            )

        else:

            self.genre.setCurrentText(
                "Other"
            )

            self.custom_genre.setText(
                genre
            )

            self.custom_genre.show()

        # -------------------------
        # Rating
        # -------------------------

        self.rating.setValue(
            book["rating"] or 0
        )

        # -------------------------
        # Reading status
        # -------------------------

        status = book.get(
            "reading_status"
        )

        if not status:

            status = (
                STATUS_FINISHED
                if book.get("is_read")
                else STATUS_WANT_TO_READ
            )

        status_display_map = {
            STATUS_WANT_TO_READ:
                "Want to Read",

            STATUS_CURRENTLY_READING:
                "Currently Reading",

            STATUS_FINISHED:
                "Finished",
        }

        self.reading_status.setCurrentText(
            status_display_map.get(
                status,
                "Want to Read"
            )
        )

        # -------------------------
        # Date read
        # -------------------------

        date_read = book.get(
            "date_read"
        )

        if date_read:

            parsed_date = QDate.fromString(
                date_read,
                "yyyy-MM-dd"
            )

            if parsed_date.isValid():

                self.date_read.setDate(
                    parsed_date
                )

        self.reading_status_changed(
            self.reading_status.currentText()
        )

        # -------------------------
        # Cover / Notes
        # -------------------------

        self.cover.setText(
            book["cover"] or ""
        )

        self.notes.setText(
            book["notes"] or ""
        )

    # =====================================================
    # Select cover
    # =====================================================

    def select_cover(
        self
    ):

        file, _ = QFileDialog.getOpenFileName(
            self,
            "Select Image",
            "",
            "Images (*.png *.jpg *.jpeg)"
        )

        if file:

            self.cover.setText(
                file
            )

    # =====================================================
    # Validate and save
    # =====================================================

    def save_book(
        self
    ):

        title = (
            self.title.text()
            .strip()
        )

        if not title:

            QMessageBox.warning(
                self,
                "Missing Title",
                "Please enter a title."
            )

            self.title.setFocus()

            return

        if (
            self.genre.currentText()
            == "Other"
            and not self.custom_genre.text().strip()
        ):

            QMessageBox.warning(
                self,
                "Missing Genre",
                "Please enter a custom genre."
            )

            self.custom_genre.setFocus()

            return

        self.accept()

    # =====================================================
    # Return book data
    # =====================================================

    def get_data(
        self
    ):

        cover_path = ""

        if self.cover.text():

            source = Path(
                self.cover.text()
            )

            images_dir = Path(
                "images"
            )

            images_dir.mkdir(
                parents=True,
                exist_ok=True
            )

            # Keep existing library image path unchanged
            if (
                    source.parent.resolve()
                    == images_dir.resolve()
            ):

                cover_path = str(
                    source
                )

            else:

                unique_name = (
                    f"{uuid4().hex}"
                    f"{source.suffix.lower()}"
                )

                destination = (
                        images_dir
                        / unique_name
                )

                shutil.copy2(
                    source,
                    destination
                )

                cover_path = str(
                    destination
                )
        # -------------------------
        # UI text -> internal status
        # -------------------------

        status_map = {
            "Want to Read":
                STATUS_WANT_TO_READ,

            "Currently Reading":
                STATUS_CURRENTLY_READING,

            "Finished":
                STATUS_FINISHED,
        }

        reading_status = status_map[
            self.reading_status.currentText()
        ]

        # -------------------------
        # Date read
        # -------------------------

        if (
            reading_status
            == STATUS_FINISHED
        ):

            date_read = (
                self.date_read.date()
                .toString(
                    "yyyy-MM-dd"
                )
            )

        else:

            date_read = None

        # -------------------------
        # Genre
        # -------------------------

        if (
            self.genre.currentText()
            == "Other"
        ):

            genre = (
                self.custom_genre.text()
                .strip()
            )

        else:

            genre = (
                self.genre.currentText()
            )

        return {

            "title":
                self.title.text().strip(),

            "author":
                self.author.text().strip(),

            "genre":
                genre,

            "rating":
                self.rating.value(),

            "pages":
                self.pages.value(),

            # Legacy compatibility
            "is_read":
                int(
                    reading_status
                    == STATUS_FINISHED
                ),

            "cover":
                cover_path,

            "notes":
                self.notes.toPlainText(),

            "reading_status":
                reading_status,

            "date_read":
                date_read,
        }

    # =====================================================
    # Custom genre
    # =====================================================

    def genre_changed(
        self,
        text
    ):

        if text == "Other":

            self.custom_genre.show()

        else:

            self.custom_genre.hide()

    # =====================================================
    # Reading status changed
    # =====================================================

    def reading_status_changed(
        self,
        status
    ):

        # `status` here is UI text,
        # not the internal constant.

        is_finished = (
            status
            == "Finished"
        )

        self.date_read_label.setVisible(
            is_finished
        )

        self.date_read.setVisible(
            is_finished
        )