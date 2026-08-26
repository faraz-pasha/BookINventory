# Book Inventory

Book Inventory is a desktop application for managing a personal book collection and tracking reading activity. It is built with Python, PySide6, and SQLite.

The application provides tools for organizing books, tracking reading status and dates, viewing library statistics, receiving book suggestions, and backing up or exporting library data.

## Features

* Add, edit, and delete books
* Store custom book cover images
* Organize books by genre
* Track books as Want to Read, Currently Reading, or Finished
* Track dates added and dates read
* Rate books and record page counts
* Add personal notes
* Search the library
* Filter books by reading status and genre
* Sort by title, author, rating, pages, date added, or date read
* View library statistics
* Generate book suggestions from the existing collection
* Back up and restore the complete library
* Export book information to CSV
* Store library information locally using SQLite

## Version History

### v1.0.0 — Core Library

Initial implementation of the book inventory system.

**Features:**

* Add, edit, and delete books
* Local SQLite database
* Title, author, and genre information
* Ratings and page counts
* Personal notes
* Custom book cover images
* Book card interface
* Detailed book views

### v1.1.0 — Library Navigation

Improved navigation and organization for larger book collections.

**Features:**

* Sidebar navigation
* Genre-based organization
* Library search
* Sorting by title, author, rating, and page count
* Dynamic book-card layout
* Scrollable library view

### v1.2.0 — Reading Status and Statistics

Expanded the application from a collection manager into a reading tracker.

**Features:**

* Want to Read, Currently Reading, and Finished statuses
* Reading-status filtering
* Genre filtering within reading statuses
* Status-specific book card styling
* Library statistics
* Statistics based on the currently selected library section
* Improved sidebar organization

### v1.3.0 — Book Suggestions

Introduced tools for selecting books to read from the existing collection.

**Features:**

* Dedicated Suggestions page
* Random book suggestions
* Genre-based suggestions
* Suggestions generated from books stored in the library
* Direct access to book details from suggestions

### v1.4.0 — Reading Dates

Added chronological information for tracking the library and reading history.

**Features:**

* Date Added tracking
* Date Read tracking
* Reading-status integration
* Sorting by Date Added
* Sorting by Date Read
* Reading-date support when editing books
* Reading dates displayed in book information

### v1.5.0 — Backup, Restore, and Export

Introduced data-management tools for protecting and exporting the library.

**Features:**

* Complete library backups in ZIP format
* User-selected backup filenames and locations
* Database and book cover images included in backups
* Restore library from a backup
* Restore both database records and cover images
* Confirmation before replacing the current library
* Export library metadata to CSV
* User-selected CSV filenames and locations
* Internal cover-image paths excluded from CSV exports
* Dedicated data-management controls in the sidebar

## Technologies

* Python 3
* PySide6
* SQLite
* Qt Style Sheets (QSS)
* CSV
* ZIP archives

## Project Structure

```text
BookINventory/
│
├── main.py
├── database.py
├── constants.py
├── backup.py
├── export.py
├── style.qss
├── requirements.txt
│
├── database/
│   └── library.db
│
├── images/
│   └── book cover images
│
├── assets/
│
└── ui/
    ├── main_window.py
    ├── add_book_dialog.py
    ├── book_card.py
    ├── book_details.py
    ├── statistics_page.py
    └── suggestion_page.py
```

The local database and user-provided book cover images are excluded from version control.

## Installation

Clone the repository:

```bash
git clone https://github.com/faraz-pasha/BookINventory.git
cd BookINventory
```

Create a virtual environment.

### macOS and Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

Run the application with:

```bash
python main.py
```

or, depending on the system:

```bash
python3 main.py
```

## Data Storage

Book Inventory stores library information locally using SQLite.

The database contains book metadata including titles, authors, genres, ratings, reading statuses, dates, page counts, notes, and references to locally stored cover images.

The database and user-provided cover images are not committed to the repository.

## Backup and Restore

The application can create a ZIP archive containing the complete local library:

```text
BookInventory_Backup.zip
│
├── library.db
└── images/
    └── ...
```

A backup can later be restored through the application, replacing the current database and cover images after user confirmation.

## CSV Export

Book metadata can be exported to a CSV file for use outside the application.

The export contains library metadata while excluding internal cover-image file paths.

## Planned Improvements

Potential future development includes:

* Richer book metadata
* Author and series organization
* Advanced reading history and statistics
* Smarter book recommendations
* Import from external data files
* ISBN support
* Automatic book metadata lookup
* Automatic cover lookup
* Integration with external book APIs

## License

This project is currently intended for personal use.
