# Defense Checklist

## Requirement Coverage

| Requirement | Implementation | Verification |
| --- | --- | --- |
| Login with username and password | `AuthService` and web login route | Default admin login |
| Add paper record | `PaperService.add_paper` and web paper form | Add form validation test |
| Delete records | Web delete route with confirmation | Browser workflow |
| Modify records | Web edit route and paper form | Update form |
| Display records | Responsive paper table with abstract preview | Browser workflow |
| Search by title or author | Search field with case-insensitive partial match | Search query test |
| Sort by publication date | Newest-first/oldest-first link | Sort query |
| Count papers by publication | Statistics page with publication bars | Grouped database query |
| Import from text file | CSV-compatible upload route | Sample CSV |
| Export to text file | UTF-8 CSV download route | Download action |
| Object Oriented Programming | ORM models and service classes | Class structure |
| Friendly GUI | Responsive FastAPI/Jinja2 web interface | Manual browser review |
| Data validity checking | Required fields, date format, future-date rule, unique ID | Unit tests |
| Main menu | Primary web navigation for Library, Statistics, Import, and Export | Manual browser review |
| Course report | Initial report document and this checklist | Report review |

## Demo Sequence

1. Start PostgreSQL.
2. Copy `.env.example` to `.env` and configure the database.
3. Run `python scripts/init_database.py`.
4. Run `python main.py`.
5. Open `http://127.0.0.1:8000`.
6. Log in using `admin / admin123`.
7. Import `data/sample_papers.csv`.
8. Search for `semantic` or an author name.
9. Toggle chronological date sorting.
10. Open Publication Statistics.
11. Add, edit, and delete a sample record.
12. Export the final records to a new CSV file.

## Talking Points

- SQLAlchemy maps database tables to Python classes, which demonstrates OOP.
- The web routes and service layers are separated, so validation and database
  behavior can be tested independently of browser rendering.
- Passwords are protected with Argon2 hashing.
- The application uses UTF-8 files, environment configuration, standard HTTP
  routes, and responsive HTML/CSS for Windows and macOS portability.

## Final Defense Extension Ideas

The current system intentionally leaves a clear extension point for novelty:

- semantic search using embeddings
- topic clustering for automatic research-area grouping
- duplicate-paper detection
- paper recommendation based on abstract similarity
- publication and keyword analytics dashboard
