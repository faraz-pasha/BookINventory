from PySide6.QtWidgets import *
import shutil
from pathlib import Path
from PySide6.QtCore import QDate

class AddBookDialog(QDialog):

    def __init__(self, book=None):

        super().__init__()
        self.setObjectName("addBookDialog")
        self.book = book
        self.setWindowTitle(
            "Edit Book"
            if book
            else "Add Book"
        )
        self.resize(400,500)


        layout = QVBoxLayout(self)


        self.title = QLineEdit()
        self.author = QLineEdit()

        self.genre = QComboBox()

        self.genre.addItems([
            "Fantasy",
            "Fiction",
            "Romance",
            "Mystery",
            "History",
            "Art",
            "Philosophy",
            "Other"
        ])

        self.genre.currentTextChanged.connect(
            self.genre_changed
        )

        self.custom_genre = QLineEdit()

        self.custom_genre.setPlaceholderText(
            "Enter custom genre"
        )

        self.custom_genre.hide()

        self.rating = QSpinBox()
        self.rating.setRange(0,5)
        self.pages = QSpinBox()

        self.pages.setRange(
            0,
            10000
        )

        self.pages.setValue(
            100
        )

        self.cover = QLineEdit()

        browse = QPushButton(
            "Choose Cover"
        )

        browse.clicked.connect(
            self.select_cover
        )

        self.reading_status = QComboBox()

        self.reading_status.addItems([
            "Want to Read",
            "Currently Reading",
            "Finished"
        ])

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

        self.reading_status.currentTextChanged.connect(
            self.reading_status_changed
        )


        self.notes = QTextEdit()


        layout.addWidget(
            QLabel("Title")
        )
        layout.addWidget(self.title)


        layout.addWidget(
            QLabel("Author")
        )
        layout.addWidget(self.author)


        layout.addWidget(
            QLabel("Genre")
        )
        layout.addWidget(self.genre)
        layout.addWidget(
            self.custom_genre
        )

        layout.addWidget(
            QLabel("Rating")
        )
        layout.addWidget(self.rating)
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
            self.accept
        )

        layout.addWidget(save)
        if book:
            self.load_book(book)

    def load_book(self, book):

        self.title.setText(
            book["title"]
        )

        self.author.setText(
            book["author"]
        )
        self.pages.setValue(
            book["pages"]
        )
        index = self.genre.findText(
            book["genre"]
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
                book["genre"]
            )

            self.custom_genre.show()
        self.rating.setValue(
            book["rating"]
        )

        status = book.get("reading_status")

        if not status:
            status = (
                "finished"
                if book["is_read"]
                else "want_to_read"
            )

        status_map = {
            "want_to_read": "Want to Read",
            "currently_reading": "Currently Reading",
            "finished": "Finished"
        }

        self.reading_status.setCurrentText(
            status_map.get(
                status,
                "Want to Read"
            )
        )

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

        self.cover.setText(
            book["cover"]
        )

        self.notes.setText(
            book["notes"]
        )


    def select_cover(self):

        file,_ = QFileDialog.getOpenFileName(
            self,
            "Select Image",
            "",
            "Images (*.png *.jpg *.jpeg)"
        )

        if file:
            self.cover.setText(file)

    def get_data(self):

        cover_path = ""

        if self.cover.text():
            source = Path(self.cover.text())

            destination = Path(
                "images"
            ) / source.name
            if source.resolve() != destination.resolve():
                shutil.copy(
                    source,
                    destination
                )

            cover_path = str(destination)

        status_map = {
            "Want to Read": "want_to_read",
            "Currently Reading": "currently_reading",
            "Finished": "finished"
        }

        reading_status = status_map[
            self.reading_status.currentText()
        ]

        if reading_status == "finished":

            date_read = (
                self.date_read.date()
                .toString("yyyy-MM-dd")
            )

        else:

            date_read = None

        return {

            "title": self.title.text(),

            "author": self.author.text(),

            "genre":
                self.custom_genre.text()
                if self.genre.currentText() == "Other"
                else self.genre.currentText(),

            "rating": self.rating.value(),

            "pages": self.pages.value(),

            "is_read": int(
                reading_status == "finished"
            ),

            "cover": cover_path,

            "notes": self.notes.toPlainText(),

            "reading_status": reading_status,

            "date_read": date_read
        }

    def genre_changed(self, text):

        if text == "Other":

            self.custom_genre.show()

        else:

            self.custom_genre.hide()

    def reading_status_changed(
            self,
            status
    ):

        is_finished = (
                status == "Finished"
        )

        self.date_read_label.setVisible(
            is_finished
        )

        self.date_read.setVisible(
            is_finished
        )
