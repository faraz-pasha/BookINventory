import sqlite3
from pathlib import Path

IMAGE_PATH = Path("images")

DB_PATH = Path("database/library.db")


def get_connection():

    DB_PATH.parent.mkdir(exist_ok=True)

    conn = sqlite3.connect(DB_PATH)

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

        notes TEXT

    )
    """)


    # Database migration
    columns = conn.execute(
        "PRAGMA table_info(books)"
    ).fetchall()


    column_names = [
        column["name"]
        for column in columns
    ]


    if "pages" not in column_names:

        conn.execute("""
        ALTER TABLE books
        ADD COLUMN pages INTEGER DEFAULT 0
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
        notes
    )

    VALUES (?, ?, ?, ?, ?, ?, ?,?)

    """,
    (
        book["title"],
        book["author"],
        book["genre"],
        book["rating"],
        book["pages"],
        book["is_read"],
        book["cover"],
        book["notes"]
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
        notes=?
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

def find_books(query):

    conn = get_connection()

    query = f"%{query}%"

    books = conn.execute(
        """
        SELECT * FROM books
        WHERE 
            title LIKE ?
            OR author LIKE ?
            OR genre LIKE ?
        """,
        (
            query,
            query,
            query
        )
    ).fetchall()

    conn.close()

    return [dict(book) for book in books]

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