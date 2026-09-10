# Research Paper Information Management Web System

Research Paper Information Management Web System is a browser-based application
for storing, searching, sorting, importing, exporting, and analyzing research
paper metadata.

The system was built for a course design defense. It follows Object Oriented
Programming principles by separating database models, business services, web
routes, and user interface templates.

## Main Features

| No. | Requirement | Status |
| --- | --- | --- |
| 1 | Login with username and password | Done |
| 2 | Add a new paper record | Done |
| 3 | Delete paper records | Done |
| 4 | Modify paper records | Done |
| 5 | Display paper records | Done |
| 6 | Search by paper title or author name | Done |
| 7 | Sort by publication date in chronological order | Done |
| 8 | Count papers by publication | Done |
| 9 | Import paper information from a text file | Done |
| 10 | Export paper information into a text file | Done |

Additional features:

- Responsive web interface.
- Main navigation menu for Library, Statistics, Import, and Export.
- Data validation for required fields, unique paper ID, date format, and future
  publication dates.
- Password hashing using Argon2.
- PostgreSQL database integration.
- CSV import and export.
- Publication statistics page.
- Legacy desktop interface kept as a fallback reference.

## Technology Stack

- Python 3.11 or newer
- FastAPI
- Uvicorn
- Jinja2
- SQLAlchemy
- PostgreSQL
- Argon2 password hashing
- HTML and CSS
- PyInstaller for packaging

## Project Structure

```text
ResearchManagement/
|-- main.py                         # Main web application entry point
|-- desktop_main.py                 # Legacy desktop entry point
|-- requirements.txt                # Python dependencies
|-- .env.example                    # Environment variable template
|-- data/
|   |-- sample_papers.csv           # Small sample import file
|   |-- dummy_papers.csv            # 10 demo paper records
|-- database/
|   |-- schema.sql                  # SQL database schema reference
|-- docs/
|   |-- SETUP_WINDOWS.md            # Detailed Windows setup guide
|   |-- DEFENSE_CHECKLIST.md        # Defense requirement checklist
|   |-- COURSE_DESIGN_REPORT.md     # Course design report source
|   |-- COURSE_DESIGN_REPORT.docx   # Course design report document
|-- scripts/
|   |-- init_database.py            # Create tables and default admin
|   |-- run_windows.ps1             # Run app on Windows
|   |-- run_mac.sh                  # Run app on macOS/Linux
|   |-- smoke_test_database.py      # Database verification script
|   |-- smoke_test_web.py           # Web workflow verification script
|-- src/research_manager/
|   |-- config.py                   # Application configuration
|   |-- database.py                 # Database engine and sessions
|   |-- models.py                   # OOP database models
|   |-- services/
|   |   |-- auth_service.py         # Authentication logic
|   |   |-- paper_service.py        # Paper CRUD, validation, import, export
|   |-- web/
|   |   |-- app.py                  # FastAPI application setup
|   |   |-- routes.py               # Web routes/controllers
|   |   |-- security.py             # Session helper functions
|   |   |-- templates/              # Jinja2 HTML templates
|   |   |-- static/styles.css       # Web interface styling
|   |-- gui/                        # Legacy PySide6 desktop interface
|-- tests/
|   |-- test_paper_service.py       # Unit tests
```

## Database Fields

Each paper record contains:

- Paper ID
- Paper title
- Authors
- Institution
- Publication
- Publication date
- Abstract
- Keywords

## Setup on Windows

### 1. Install Required Tools

Install these tools first:

- Python 3.11 or newer
- PostgreSQL 14 or newer
- Visual Studio Code
- Git, optional but recommended

When installing Python on Windows, enable **Add Python.exe to PATH**.

### 2. Open Project

Open this folder in VS Code:

```text
C:\ResearchManagement
```

Open the VS Code terminal and check Python:

```powershell
python --version
```

### 3. Create Virtual Environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If PowerShell blocks activation, run:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Then activate the virtual environment again.

### 4. Configure PostgreSQL

Create a PostgreSQL database:

```text
research_management
```

Copy the environment template:

```powershell
Copy-Item .env.example .env
```

Open `.env` and update the database password:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=research_management
DB_USER=postgres
DB_PASSWORD=your_postgresql_password
APP_SECRET_KEY=replace_with_a_long_random_secret
APP_HOST=127.0.0.1
APP_PORT=8000
```

For a quick development secret, you can generate one with:

```powershell
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 5. Initialize Database

```powershell
python scripts/init_database.py
```

Expected output:

```text
Database tables are ready.
Default login: admin / admin123
```

### 6. Run Web Application

```powershell
python main.py
```

Or:

```powershell
.\scripts\run_windows.ps1
```

Open the application in a browser:

```text
http://127.0.0.1:8000
```

Default login:

```text
Username: admin
Password: admin123
```

## Setup on macOS

This project can also be moved to an Intel MacBook or Apple Silicon Mac.

### 1. Install Required Tools

Install:

- Python 3.11 or newer
- PostgreSQL 14 or newer
- Visual Studio Code
- Git, optional but recommended

Homebrew can be used on macOS:

```bash
brew install python postgresql
```

### 2. Create Virtual Environment

From the project folder:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 3. Configure Database

Create the `research_management` PostgreSQL database, then copy and edit the
environment file:

```bash
cp .env.example .env
```

Update the PostgreSQL username and password in `.env`.

### 4. Initialize and Run

```bash
python scripts/init_database.py
python main.py
```

Or:

```bash
sh scripts/run_mac.sh
```

Open:

```text
http://127.0.0.1:8000
```

## Import and Export Format

The application imports and exports CSV files. CSV is a text-file format, so it
satisfies the requirement to import and export paper information from and into a
text file.

Required CSV columns:

```text
paper_id,title,authors,institution,publication,publication_date,abstract,keywords
```

Date format:

```text
YYYY-MM-DD
```

Example import files:

```text
data/sample_papers.csv
data/dummy_papers.csv
```

## Demo Data

The file `data/dummy_papers.csv` contains 10 ready-to-use dummy records:

```text
DUMMY-001 ... DUMMY-010
```

To import them:

1. Start the application.
2. Login as admin.
3. Open the **Import** menu.
4. Choose `data/dummy_papers.csv`.
5. Submit the form.
6. Return to **Library**.

## Testing

Run unit tests:

```bash
pytest
```

Run code quality check:

```bash
ruff check .
```

Run database smoke test:

```bash
python scripts/smoke_test_database.py
```

Run web smoke test after starting the web server:

```bash
python scripts/smoke_test_web.py
```

## Packaging

### Windows Executable

```powershell
pyinstaller --noconfirm --clean --paths src --name ResearchPaperManager `
  --add-data "src/research_manager/web/templates;research_manager/web/templates" `
  --add-data "src/research_manager/web/static;research_manager/web/static" `
  main.py
```

The generated executable is placed in:

```text
dist\ResearchPaperManager\ResearchPaperManager.exe
```

Before running the executable, copy the configured `.env` file into:

```text
dist\ResearchPaperManager\
```

PostgreSQL must still be installed and running separately.

### macOS App Build

Run this command on the target Mac:

```bash
pyinstaller --noconfirm --clean --paths src --name ResearchPaperManager \
  --add-data "src/research_manager/web/templates:research_manager/web/templates" \
  --add-data "src/research_manager/web/static:research_manager/web/static" \
  main.py
```

The packaged application does not include PostgreSQL or database data.

## Suggested Defense Demonstration Flow

1. Start PostgreSQL.
2. Run `python main.py`.
3. Open `http://127.0.0.1:8000`.
4. Login using `admin / admin123`.
5. Display all paper records in **Library**.
6. Import `data/dummy_papers.csv`.
7. Search by a title keyword, for example `Machine Learning`.
8. Search by an author name, for example `Nadia`.
9. Sort by publication date.
10. Add a new paper manually.
11. Edit the new paper.
12. Delete a selected paper.
13. Open **Statistics** to show count by publication.
14. Export all records to CSV.

## OOP Design Summary

The project uses Object Oriented Programming through:

- `User` and `Paper` ORM model classes.
- `AuthService` for login and password verification logic.
- `PaperService` for validation, CRUD, search, sorting, statistics, import, and
  export.
- Web route functions that call service classes instead of directly mixing all
  business logic into the interface.

This separation makes the system easier to test, explain, maintain, and extend.

## Future Novelty Ideas for Final Defense

The current version completes the required system. For the final defense, these
technical methods can be discussed with the supervisor:

- Semantic search using text embeddings.
- Topic clustering from abstracts and keywords.
- Duplicate paper detection using title and abstract similarity.
- Paper recommendation based on research topic similarity.
- Dashboard analytics for publication trends and institution collaboration.
- DOI metadata auto-fill from external scholarly APIs.

## Security Notes

- Change the default admin password before real use.
- Use a long random `APP_SECRET_KEY`.
- Keep `.env` private.
- Do not commit database passwords to Git.
- Use HTTPS if the system is deployed on a public server.

## Current Application Type

The official version of this project is a **web-based system**.

The previous desktop interface is kept only as a backup/reference:

```bash
python desktop_main.py
```
