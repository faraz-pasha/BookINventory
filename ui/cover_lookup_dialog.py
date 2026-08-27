import urllib.request

from PySide6.QtCore import (
    Qt,
    QSize,
)

from PySide6.QtGui import (
    QPixmap,
)

from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QMessageBox,
)


class CoverLookupDialog(QDialog):

    def __init__(
        self,
        results,
        parent=None,
    ):

        super().__init__(
            parent
        )

        self.setObjectName(
            "coverLookupDialog"
        )

        self.setWindowTitle(
            "Choose Cover"
        )

        self.resize(
            700,
            450
        )

        self.results = results
        self.selected_cover_url = ""

        layout = QVBoxLayout(
            self
        )

        title = QLabel(
            "Choose a cover"
        )

        title.setObjectName(
            "coverLookupTitle"
        )

        layout.addWidget(
            title
        )

        self.cover_list = QListWidget()

        self.cover_list.setObjectName(
            "coverLookupResults"
        )

        self.cover_list.setViewMode(
            QListWidget.IconMode
        )

        self.cover_list.setResizeMode(
            QListWidget.Adjust
        )

        self.cover_list.setMovement(
            QListWidget.Static
        )

        self.cover_list.setSpacing(
            12
        )

        self.cover_list.setIconSize(
            QSize(
                120,
                180
            )
        )

        layout.addWidget(
            self.cover_list
        )

        self.populate_covers()

        button_row = QHBoxLayout()

        no_cover_button = QPushButton(
            "No Cover"
        )

        no_cover_button.setObjectName(
            "noCoverButton"
        )

        no_cover_button.clicked.connect(
            self.no_cover
        )

        select_button = QPushButton(
            "Use Selected Cover"
        )

        select_button.setObjectName(
            "coverSelectButton"
        )

        select_button.clicked.connect(
            self.select_cover
        )

        button_row.addWidget(
            no_cover_button
        )

        button_row.addStretch()

        button_row.addWidget(
            select_button
        )

        layout.addLayout(
            button_row
        )

        self.cover_list.itemDoubleClicked.connect(
            self.select_cover
        )

    def populate_covers(
        self
    ):

        seen_urls = set()

        for book in self.results:

            cover_url = (
                book.get(
                    "cover_url"
                )
                or ""
            )

            if not cover_url:
                continue

            if cover_url in seen_urls:
                continue

            seen_urls.add(
                cover_url
            )

            pixmap = self.load_cover(
                cover_url
            )

            if pixmap is None:
                continue

            item = QListWidgetItem()

            item.setData(
                Qt.UserRole,
                cover_url
            )

            item.setIcon(
                pixmap
            )

            published_date = (
                    book.get(
                        "published_date"
                    )
                    or ""
            )

            item.setText(
                published_date
            )

            item.setTextAlignment(
                Qt.AlignCenter
            )

            item.setSizeHint(
                QSize(
                    150,
                    230
                )
            )

            self.cover_list.addItem(
                item
            )

    def load_cover(
        self,
        cover_url
    ):

        if cover_url.startswith(
            "http://"
        ):

            cover_url = (
                "https://"
                + cover_url[
                    len("http://"):
                ]
            )

        try:

            request = urllib.request.Request(
                cover_url,
                headers={
                    "User-Agent":
                        "BookInventory"
                }
            )

            with urllib.request.urlopen(
                request,
                timeout=10
            ) as response:

                image_data = (
                    response.read()
                )

            pixmap = QPixmap()

            if not pixmap.loadFromData(
                image_data
            ):

                return None

            return pixmap.scaled(
                120,
                180,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation,
            )

        except Exception:

            return None

    def select_cover(
            self,
            item=None
    ):

        if not isinstance(
                item,
                QListWidgetItem
        ):
            item = (
                self.cover_list
                .currentItem()
            )

        if item is None:
            QMessageBox.warning(
                self,
                "No Cover Selected",
                "Please select a cover."
            )

            return

        self.selected_cover_url = (
            item.data(
                Qt.UserRole
            )
        )

        self.accept()

    def no_cover(
        self
    ):

        self.selected_cover_url = ""

        self.accept()

    def get_selected_cover(
        self
    ):

        return self.selected_cover_url