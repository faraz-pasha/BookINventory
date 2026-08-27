import sqlite3
from datetime import date

from constants import (
    STATUS_WANT_TO_READ,
    STATUS_FINISHED,
)

from app_paths import (
    DB_PATH,
    migrate_legacy_data,
)


# ============================================================
# Database connection
# ============================================================

def get_connection():

    DB_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    conn = sqlite3.connect(
        DB_PATH
    )

    conn.row_factory = sqlite3.Row

    return conn


# ============================================================
# Database initialization
# ============================================================

def initialize_database():

    migrate_legacy_data()

    conn = get_connection()

    conn.execute(f"""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            title TEXT NOT NULL,
            author TEXT,
            genre TEXT,

            rating INTEGER DEFAULT 0,
            pages INTEGER DEFAULT 0,

            is_read INTEGER DEFAULT 0,

            cover TEXT,
            notes TEXT,

            isbn TEXT,
            description TEXT,
            
            reading_status TEXT
            DEFAULT '{STATUS_WANT_TO_READ}',
            
            date_added TEXT,
            date_read TEXT
        )
    """)

    migrate_database(
        conn
    )

    conn.commit()
    conn.close()


# ============================================================
# Database migrations
# ============================================================

def migrate_database(conn):

    columns = conn.execute(
        "PRAGMA table_info(books)"
    ).fetchall()

    column_names = {
        column["name"]
        for column in columns
    }

    # --------------------------------------------------------
    # Pages
    # --------------------------------------------------------

    if "pages" not in column_names:

        conn.execute("""
            ALTER TABLE books
            ADD COLUMN pages INTEGER DEFAULT 0
        """)

    # --------------------------------------------------------
    # Reading status
    # --------------------------------------------------------

    if "reading_status" not in column_names:

        conn.execute(f"""
            ALTER TABLE books
            ADD COLUMN reading_status TEXT
            DEFAULT '{STATUS_WANT_TO_READ}'
        """)

    # --------------------------------------------------------
    # Date added
    # --------------------------------------------------------

    if "date_added" not in column_names:

        conn.execute("""
            ALTER TABLE books
            ADD COLUMN date_added TEXT
        """)

    # --------------------------------------------------------
    # Date read
    # --------------------------------------------------------

    if "date_read" not in column_names:

        conn.execute("""
            ALTER TABLE books
            ADD COLUMN date_read TEXT
        """)
    # --------------------------------------------------------
    # ISBN
    # --------------------------------------------------------

    if "isbn" not in column_names:
        conn.execute("""
        ALTER TABLE books
        ADD COLUMN isbn TEXT
        """)

    # --------------------------------------------------------
    # Description
    # --------------------------------------------------------

    if "description" not in column_names:
        conn.execute("""
        ALTER TABLE books
        ADD COLUMN description TEXT
        """)
    # --------------------------------------------------------
    # Convert old is_read values to reading_status
    # --------------------------------------------------------

    conn.execute(
        """
        UPDATE books
        SET reading_status = ?
        WHERE reading_status IS NULL
          AND is_read = 1
        """,
        (
            STATUS_FINISHED,
        )
    )

    conn.execute(
        """
        UPDATE books
        SET reading_status = ?
        WHERE reading_status IS NULL
          AND is_read = 0
        """,
        (
            STATUS_WANT_TO_READ,
        )
    )


# ============================================================
# Add book
# ============================================================

def add_book(book):

    conn = get_connection()

    conn.execute(
        """
        INSERT INTO books
        (
            title,
            author,
            genre,
            rating,
            pages,
            is_read,
            cover,
            notes,
            isbn,
            description,
            reading_status,
            date_added,
            date_read
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            book["title"],
            book["author"],
            book["genre"],
            book["rating"],
            book["pages"],
            book["is_read"],
            book["cover"],
            book["notes"],
            book.get("isbn"),
            book.get("description"),
            book["reading_status"],
            date.today().isoformat(),
            book.get("date_read"),
        )
    )

    conn.commit()
    conn.close()


# ============================================================
# Get books
# ============================================================

def get_books():

    conn = get_connection()

    rows = conn.execute(
        "SELECT * FROM books"
    ).fetchall()

    conn.close()

    return [
        dict(row)
        for row in rows
    ]


# ============================================================
# Update book
# ============================================================

def update_book(
    book_id,
    book
):

    conn = get_connection()

    conn.execute(
        """
        UPDATE books
        SET
            title = ?,
            author = ?,
            genre = ?,
            rating = ?,
            pages = ?,
            is_read = ?,
            cover = ?,
            notes = ?,
            isbn = ?,
            description = ?,
            reading_status = ?,
            date_read = ?
        WHERE id = ?
        """,
        (
            book["title"],
            book["author"],
            book["genre"],
            book["rating"],
            book["pages"],
            book["is_read"],
            book["cover"],
            book["notes"],
            book.get("isbn"),
            book.get("description"),
            book["reading_status"],
            book.get("date_read"),
            book_id,
        )
    )



    conn.commit()
    conn.close()

# ============================================================
# Update reading status
# ============================================================

def update_book_status(
    book_id,
    new_status
):

    conn = get_connection()

    # Keep legacy is_read field synchronized
    is_read = (
        1
        if new_status == STATUS_FINISHED
        else 0
    )

    # If marking as finished for the first time,
    # automatically store today's date.
    if new_status == STATUS_FINISHED:

        conn.execute(
            """
            UPDATE books
            SET
                reading_status = ?,
                is_read = ?,
                date_read = COALESCE(
                    date_read,
                    ?
                )
            WHERE id = ?
            """,
            (
                new_status,
                is_read,
                date.today().isoformat(),
                book_id,
            )
        )

    else:

        conn.execute(
            """
            UPDATE books
            SET
                reading_status = ?,
                is_read = ?
            WHERE id = ?
            """,
            (
                new_status,
                is_read,
                book_id,
            )
        )

    conn.commit()
    conn.close()


# ============================================================
# Delete book
# ============================================================

def delete_book(book_id):

    conn = get_connection()

    conn.execute(
        """
        DELETE FROM books
        WHERE id = ?
        """,
        (
            book_id,
        )
    )

    conn.commit()
    conn.close()

# ============================================================
# Update rating
# ============================================================

def update_book_rating(
    book_id,
    rating
):

    conn = get_connection()

    conn.execute(
        """
        UPDATE books
        SET rating = ?
        WHERE id = ?
        """,
        (
            rating,
            book_id,
        )
    )

    conn.commit()
    conn.close()

