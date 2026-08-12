import sqlite3
from pathlib import Path

IMAGE_PATH = Path("images")

DB_PATH = Path("database/library.db")


def get_connection():

    DB_PATH.parent.mkdir(
        exist_ok=True
    )

    conn = sqlite3.connect(
        DB_PATH
    )

    conn.row_factory = sqlite3.Row

    conn.execute("""
        CREATE TABLE IF NOT EXISTS books(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            title TEXT NOT NULL,
            author TEXT,

            genre TEXT,

            rating INTEGER DEFAULT 0,

            is_read INTEGER DEFAULT 0,

            cover TEXT,

            notes TEXT,

            reading_status TEXT
                DEFAULT 'want_to_read'
        )
    """)

    # -------------------------
    # Database migrations
    # -------------------------

    columns = conn.execute(
        "PRAGMA table_info(books)"
    ).fetchall()

    column_names = [
        column["name"]
        for column in columns
    ]

    # Add pages column if it
    # does not already exist

    if "pages" not in column_names:

        conn.execute("""
            ALTER TABLE books
            ADD COLUMN pages INTEGER
            DEFAULT 0
        """)

    # Add reading_status column
    # if it does not already exist

    if "reading_status" not in column_names:
        conn.execute("""
            ALTER TABLE books
            ADD COLUMN reading_status TEXT
            DEFAULT 'want_to_read'
        """)

    # -------------------------
    # Migrate reading status
    # -------------------------

    conn.execute("""
        UPDATE books
        SET reading_status = 'finished'
        WHERE reading_status IS NULL
          AND is_read = 1
    """)

    conn.execute("""
        UPDATE books
        SET reading_status = 'want_to_read'
        WHERE reading_status IS NULL
          AND is_read = 0
    """)

    conn.commit()

    return conn



def add_book(book):

    conn = get_connection()

    conn.execute("""
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
            reading_status
        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)

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
        book["reading_status"]
    ))

    conn.commit()

    conn.close()



def get_books():

    conn = get_connection()

    rows = conn.execute(
        "SELECT * FROM books"
    ).fetchall()

    conn.close()

    return [dict(row) for row in rows]

def update_book(book_id, book):

    conn = get_connection()

    conn.execute("""
        UPDATE books
        SET
            title=?,
            author=?,
            genre=?,
            rating=?,
            pages=?,
            is_read=?,
            cover=?,
            notes=?,
            reading_status=?
        WHERE id=?
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
        book["reading_status"],
        book_id
    ))

    conn.commit()

    conn.close()

def delete_book(book_id):

    conn = get_connection()

    conn.execute(
        """
        DELETE FROM books
        WHERE id=?
        """,
        (book_id,)
    )

    conn.commit()
    conn.close()

def get_genre_counts():

    conn = get_connection()

    genres = conn.execute(
        """
        SELECT 
            genre,
            COUNT(*) as count
        FROM books
        WHERE genre IS NOT NULL
        GROUP BY genre
        ORDER BY genre
        """
    ).fetchall()

    conn.close()

    return [
        dict(row)
        for row in genres
    ]