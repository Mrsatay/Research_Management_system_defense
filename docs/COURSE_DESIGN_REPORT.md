# Research Paper Information Management System

## 1 Introduction

This project implements a web-based research paper information management system.
The system stores paper ID, title, authors, institution, publication, publication
date, abstract, and keywords. It provides authenticated access and the complete
record-management workflow required by the course design brief.

The current version is the defense baseline. It focuses on reliable CRUD
operations, clear validation, database persistence, file exchange, and a
maintainable object-oriented structure. A later final-defense version can extend
this foundation with a novel intelligent method.

## 2 Objectives

The objectives are to:

- provide a structured repository for research paper metadata;
- support secure username and password login;
- provide add, edit, delete, display, search, sort, and counting operations;
- import and export records through a text-compatible CSV format;
- demonstrate object-oriented programming through models and service classes;
- provide a usable responsive web interface with clear primary navigation.

## 3 Functional Requirements

The system supports:

1. login with username and password;
2. adding a paper record;
3. deleting one or more records;
4. modifying a selected record;
5. displaying all records;
6. searching by paper title or author;
7. sorting by publication date;
8. counting records by publication;
9. importing paper information from a text file;
10. exporting all paper information to a text file.

## 4 Technology Selection

The application is implemented with Python, FastAPI, and Jinja2. FastAPI
provides the web application and HTTP routing, while Jinja2 renders server-side
HTML templates. SQLAlchemy provides an object-relational mapping layer, allowing
database tables to be represented by Python classes. PostgreSQL is used for
persistent storage. Psycopg is the PostgreSQL driver.

The project uses a virtual environment and stores secrets in `.env`. The system
can be opened from a browser on Windows, macOS, or Linux. Uvicorn runs the local
development server and can later be placed behind a production reverse proxy.

## 5 System Architecture

The system follows a lightweight layered web architecture:

- `models.py` defines the `User` and `Paper` ORM entities.
- `database.py` creates the SQLAlchemy engine and transaction scope.
- `auth_service.py` handles password hashing and authentication.
- `paper_service.py` handles validation, CRUD, search, sorting, statistics,
  import, and export.
- `web/app.py` creates the FastAPI application, sessions, templates, and static
  files.
- `web/routes.py` provides authentication, CRUD, search, sorting, statistics,
  import, and export routes.
- `web/templates/` contains the responsive HTML pages.
- `web/static/styles.css` contains the visual system for the browser interface.
- `app.py` initializes the database and starts the web server.

This separation keeps route handling focused on HTTP interaction and keeps
business rules testable independently.

## 6 Database Design

### 6.1 Users Table

| Field | Type | Constraint |
| --- | --- | --- |
| id | integer | primary key |
| username | varchar | unique, required |
| password_hash | varchar | required |
| created_at | timestamp | required |

### 6.2 Papers Table

| Field | Type | Constraint |
| --- | --- | --- |
| id | integer | primary key |
| paper_id | varchar | unique, required |
| title | varchar | required |
| authors | varchar | required |
| institution | varchar | required |
| publication | varchar | required |
| publication_date | date | required |
| abstract | text | required |
| keywords | varchar | required |
| created_at | timestamp | required |
| updated_at | timestamp | required |

Indexes are added to paper ID, title, authors, publication, and publication
date to support common management and search operations.

## 7 Data Validation

The service layer trims text input and checks every required field. Publication
dates must use `YYYY-MM-DD` and cannot be in the future. Paper IDs are unique in
the database. Invalid records are rejected with a user-readable message before
the dialog closes.

User passwords are hashed with Argon2. The application never stores the
original password as a database value.

## 8 Web Interface Design

The web interface contains:

- a login page;
- Library, Statistics, Import, and Export navigation;
- a searchable research paper table;
- add, edit, and delete actions;
- expandable abstract previews;
- visible record count and sort direction;
- responsive layouts for desktop and mobile browser widths.

The interface uses a restrained blue and neutral palette, readable data-dense
tables, confirmation before deletion, and a browser-native date selector.

## 9 File Format

Import and export use UTF-8 CSV, which is a text file format supported by common
spreadsheet and text editors. The header is:

`paper_id,title,authors,institution,publication,publication_date,abstract,keywords`

Import validates each row independently and reports skipped rows while keeping
valid rows. Export writes all records in chronological order.

## 10 Testing

The current automated tests verify:

- valid date conversion;
- rejection of missing required fields;
- rejection of future publication dates;
- web login, CRUD, search, statistics, import, and export smoke workflow.

The project also passes Python compilation and Ruff code-quality checks. The
database-backed workflow is tested after the PostgreSQL password is configured
in `.env`.

## 11 Requirement Traceability

The file `docs/DEFENSE_CHECKLIST.md` maps each course requirement to its source
implementation and suggested defense demonstration.

## 12 Future Work and Novelty Direction

The baseline system is intentionally designed so intelligent features can be
added without rewriting the CRUD foundation. Possible final-defense research
directions include semantic search with document embeddings, automatic topic
clustering, duplicate-paper detection, or paper recommendation based on
abstract similarity.

One possible future title is:

**Intelligent Research Paper Information Management System Using Semantic Search
and Topic Clustering**

The final method should be selected with the supervisor after the baseline has
been evaluated.

## 13 Conclusion

The project provides a complete starting implementation for a web-based research
paper information management system. It meets the required management
operations, uses an object-oriented architecture, persists data in PostgreSQL,
validates input, and provides a browser-based foundation for the final-defense
extension.
