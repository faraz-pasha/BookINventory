from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
    QProgressBar,
    QScrollArea,
)
from PySide6.QtCore import Qt

from constants import (
    STATUS_WANT_TO_READ,
    STATUS_CURRENTLY_READING,
    STATUS_FINISHED,
)

class StatisticsPage(QWidget):

    def __init__(self):

        super().__init__()

        self.setObjectName(
            "statisticsPage"
        )

        # Main layout
        outer_layout = QVBoxLayout(self)

        outer_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        # Scroll area
        self.scroll_area = QScrollArea()

        self.scroll_area.setWidgetResizable(
            True
        )

        self.scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff
        )

        self.scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarAsNeeded
        )

        # Content widget
        self.scroll_content = QWidget()

        self.scroll_content.setObjectName(
            "statisticsScrollContent"
        )

        self.main_layout = QVBoxLayout(
            self.scroll_content
        )

        self.main_layout.setContentsMargins(
            25,
            25,
            25,
            25
        )

        self.main_layout.setSpacing(
            20
        )

        self.scroll_area.setWidget(
            self.scroll_content
        )

        outer_layout.addWidget(
            self.scroll_area
        )

        self.build_empty_page()

    def build_empty_page(self):

        title = QLabel(
            "📊 Library Statistics"
        )

        title.setObjectName(
            "statisticsTitle"
        )

        self.main_layout.addWidget(
            title
        )

        self.content = QWidget()

        self.content_layout = QVBoxLayout(
            self.content
        )

        self.content_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        self.content_layout.setSpacing(
            20
        )

        self.main_layout.addWidget(
            self.content
        )

        self.main_layout.addStretch()

    def clear_content(
            self
    ):

        self.clear_layout(
            self.content_layout,
            delete_layout=False
        )

    def clear_layout(
            self,
            layout,
            delete_layout=True
    ):

        while layout.count():

            item = layout.takeAt(
                0
            )

            widget = item.widget()

            child_layout = item.layout()

            if widget:

                widget.deleteLater()

            elif child_layout:

                self.clear_layout(
                    child_layout
                )

        if delete_layout:
            layout.deleteLater()


    def create_stat_card(
        self,
        value,
        label
    ):

        card = QFrame()

        card.setObjectName(
            "statCard"
        )

        layout = QVBoxLayout(
            card
        )

        layout.setAlignment(
            Qt.AlignCenter
        )

        value_label = QLabel(
            str(value)
        )

        value_label.setObjectName(
            "statValue"
        )

        value_label.setAlignment(
            Qt.AlignCenter
        )

        label_widget = QLabel(
            label
        )

        label_widget.setObjectName(
            "statLabel"
        )

        label_widget.setAlignment(
            Qt.AlignCenter
        )

        layout.addWidget(
            value_label
        )

        layout.addWidget(
            label_widget
        )

        return card


    def create_section(
        self,
        title
    ):

        frame = QFrame()

        frame.setObjectName(
            "statisticsSection"
        )

        layout = QVBoxLayout(
            frame
        )

        heading = QLabel(
            title
        )

        heading.setObjectName(
            "statisticsSectionTitle"
        )

        layout.addWidget(
            heading
        )

        return frame, layout


    def update_statistics(
        self,
        books,
        title="Library Statistics"
    ):

        self.clear_content()

        # -------------------------
        # Title
        # -------------------------

        self.findChild(
            QLabel,
            "statisticsTitle"
        ).setText(
            f"📊 {title}"
        )


        # -------------------------
        # Basic statistics
        # -------------------------

        total = len(books)

        want_to_read = sum(
            1
            for book in books
            if book["reading_status"]
            == STATUS_WANT_TO_READ
        )

        currently_reading = sum(
            1
            for book in books
            if book["reading_status"]
            == STATUS_CURRENTLY_READING
        )

        finished = sum(
            1
            for book in books
            if book["reading_status"]
            == STATUS_FINISHED
        )

        total_pages = sum(
            book["pages"] or 0
            for book in books
        )

        rated_books = [
            book
            for book in books
            if (book["rating"] or 0) > 0
        ]

        if rated_books:

            average_rating = (
                    sum(
                        book["rating"]
                        for book in rated_books
                    )
                    / len(rated_books)
            )

        else:

            average_rating = None


        # -------------------------
        # Statistic cards
        # -------------------------

        cards = QHBoxLayout()

        cards.setSpacing(
            15
        )

        cards.addWidget(
            self.create_stat_card(
                total,
                "Total Books"
            )
        )

        cards.addWidget(
            self.create_stat_card(
                want_to_read,
                "Want to Read"
            )
        )

        cards.addWidget(
            self.create_stat_card(
                currently_reading,
                "Currently Reading"
            )
        )

        cards.addWidget(
            self.create_stat_card(
                finished,
                "Finished"
            )
        )

        cards.addWidget(
            self.create_stat_card(
                f"{total_pages:,}",
                "Total Pages"
            )
        )

        cards.addWidget(
            self.create_stat_card(
                (
    f"{average_rating:.1f} ★"
    if average_rating is not None
    else "N/A"
),
                "Average Rating"
            )
        )

        self.content_layout.addLayout(
            cards
        )


        # -------------------------
        # Reading progress
        # -------------------------

        progress_frame, progress_layout = (
            self.create_section(
                "📖 Reading Progress"
            )
        )

        progress = QProgressBar()

        progress.setRange(
            0,
            max(total, 1)
        )

        progress.setValue(
            finished
        )

        progress.setFormat(
            f"{finished} / {total} books finished"
        )


        progress.setTextVisible(
            True
        )

        progress_layout.addWidget(
            progress
        )

        self.content_layout.addWidget(
            progress_frame
        )


        # -------------------------
        # Genre statistics
        # -------------------------

        genre_frame, genre_layout = (
            self.create_section(
                "📚 Books by Genre"
            )
        )

        genre_counts = {}

        for book in books:

            genre = (
                book["genre"]
                or "Unknown"
            )

            genre_counts[genre] = (
                genre_counts.get(
                    genre,
                    0
                ) + 1
            )


        if genre_counts:

            max_count = max(
                genre_counts.values()
            )

            for genre, count in sorted(
                genre_counts.items(),
                key=lambda x: x[1],
                reverse=True
            ):

                row = QHBoxLayout()

                label = QLabel(
                    genre
                )

                label.setMinimumWidth(
                    120
                )

                bar = QProgressBar()

                bar.setRange(
                    0,
                    max_count
                )

                bar.setValue(
                    count
                )

                bar.setFormat(
                    f"{count}"
                )

                row.addWidget(
                    label
                )

                row.addWidget(
                    bar
                )

                genre_layout.addLayout(
                    row
                )

        else:

            genre_layout.addWidget(
                QLabel(
                    "No genre data available."
                )
            )


        self.content_layout.addWidget(
            genre_frame
        )


        # -------------------------
        # Rating distribution
        # -------------------------

        rating_frame, rating_layout = (
            self.create_section(
                "⭐ Rating Distribution"
            )
        )

        rating_counts = {
            1: 0,
            2: 0,
            3: 0,
            4: 0,
            5: 0
        }

        for book in books:

            rating = book["rating"] or 0

            if rating in rating_counts:

                rating_counts[rating] += 1


        max_rating_count = max(
            rating_counts.values(),
            default=1
        )

        for rating in range(
            5,
            0,
            -1
        ):

            row = QHBoxLayout()

            label = QLabel(
                "★" * rating
            )

            label.setMinimumWidth(
                80
            )

            bar = QProgressBar()

            bar.setRange(
                0,
                max_rating_count
            )

            bar.setValue(
                rating_counts[rating]
            )

            bar.setFormat(
                str(
                    rating_counts[rating]
                )
            )

            row.addWidget(
                label
            )

            row.addWidget(
                bar
            )

            rating_layout.addLayout(
                row
            )


        self.content_layout.addWidget(
            rating_frame
        )


        # -------------------------
        # Highlights
        # -------------------------

        highlights_frame, highlights_layout = (
            self.create_section(
                "🏆 Highlights"
            )
        )


        if books:
            rated_books = [
                book
                for book in books
                if (book["rating"] or 0) > 0
            ]

            if rated_books:

                highest_rated = max(
                    rated_books,
                    key=lambda b: b["rating"]
                )

                highest_rated_text = (
                    f"{highest_rated['title']} "
                    f"({highest_rated['rating']} ★)"
                )

            else:

                highest_rated_text = "No rated books"

            longest_book = max(
                books,
                key=lambda b: (
                    b["pages"] or 0
                )
            )

            most_common_genre = (
                max(
                    genre_counts,
                    key=genre_counts.get
                )
                if genre_counts
                else "N/A"
            )


            highlights = [
                (
                    "⭐ Highest Rated",
                    highest_rated_text
                ),
                (
                    "📖 Longest Book",
                    f"{longest_book['title']} "
                    f"({longest_book['pages'] or 0:,} pages)"
                ),
                (
                    "📚 Most Common Genre",
                    f"{most_common_genre} "
                    f"({genre_counts.get(most_common_genre, 0)} books)"
                )
            ]


            for label_text, value_text in highlights:

                row = QHBoxLayout()

                label = QLabel(
                    label_text
                )

                label.setObjectName(
                    "highlightLabel"
                )

                value = QLabel(
                    value_text
                )

                value.setWordWrap(
                    True
                )

                row.addWidget(
                    label
                )

                row.addWidget(
                    value
                )

                highlights_layout.addLayout(
                    row
                )

        else:

            highlights_layout.addWidget(
                QLabel(
                    "No books in this selection."
                )
            )


        self.content_layout.addWidget(
            highlights_frame
        )

        self.content_layout.addStretch()