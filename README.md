# Book Inventory App

A desktop book inventory and reading-tracking application built with **Python** and **PySide6**. The application provides a visual interface for organizing a personal book collection, tracking reading status, and managing book information.

## Features

* Add books to your personal library
* Edit existing book information
* Delete books
* Organize books by genre
* Track whether a book has been read
* Search for books
* Sort books by:

  * Title
  * Author
  * Rating
  * Number of pages
* View detailed information about individual books
* Add notes to books
* Store book information in a local SQLite database
* Visual book cards for browsing the collection
* Custom styling using Qt Style Sheets (`.qss`)

## Technologies

* **Python**
* **PySide6** — graphical user interface
* **SQLite** — local database
* **Qt Style Sheets (QSS)** — application styling

## Project Structure

```text
book-inventory/
│
├── main.py                 # Application entry point
├── database.py             # Database operations
├── models.py               # Application data models
├── style.qss               # Application styling
├── .gitignore              # Files excluded from Git
│
├── database/               # Local database files
│
├── ui/                     # User interface components
│   ├── add_book_dialog.py
│   ├── book_card.py
│   ├── book_details.py
│   └── ...
│
└── images/                 # Local book images
```

The local SQLite database and user-provided images are excluded from version control.

## Requirements

* Python 3.x
* PySide6

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd book-inventory
```

Create a virtual environment:

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

Install the required dependencies:

```bash
pip install PySide6
```

## Running the Application

From the project directory:

```bash
python main.py
```

On macOS, you may need to use:

```bash
python3 main.py
```

## Database

The application uses **SQLite** for local book storage. The database is created and managed locally by the application.

The local database file is intentionally excluded from Git because it contains user-specific library data.

## Git Workflow

This project uses Git for version control.

A typical development workflow is:

```bash
git pull

# Make changes

git status
git add .
git commit -m "Describe your changes"
git push
```

For new features, create a separate branch:

```bash
git switch -c feature/my-feature
```

After completing the feature, push the branch and create a pull request on GitHub.

## Future Improvements

Potential future additions include:

* Book cover management
* Improved filtering
* Reading progress tracking
* Book recommendations
* Statistics and reading analytics
* Import/export functionality
* ISBN lookup
* Integration with external book APIs
* Improved database management and backup

## License

This project is currently for personal use.
