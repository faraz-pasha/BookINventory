from PySide6.QtWidgets import *
import shutil
from pathlib import Path

class AddBookDialog(QDialog):

    def __init__(self, book=None):

        super().__init__()
        self.setObjectName("addBookDialog")
        self.book = book
        self.setWindowTitle(
            "Add Book"
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
            1,
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


        self.read = QCheckBox(
            "I have read this book"
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
            self.read
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

        self.read.setChecked(
            bool(book["is_read"])
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
                self.read.isChecked()
            ),

            "cover": cover_path,

            "notes": self.notes.toPlainText()

        }

    def genre_changed(self, text):

        if text == "Other":

            self.custom_genre.show()

        else:

            self.custom_genre.hide()
