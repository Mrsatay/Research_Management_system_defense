# Windows Setup Guide

## 1 Open the Project

Open `C:\ResearchManagement` in VS Code.

Open the integrated PowerShell terminal and confirm that the terminal is using
the same Python installation where the project packages were installed:

```powershell
python --version
```

If Python is not found, reinstall Python with **Add Python.exe to PATH** enabled,
then restart VS Code.

## 2 Create the Virtual Environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If PowerShell blocks activation:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

## 3 Configure PostgreSQL

Make sure the PostgreSQL service is running. In pgAdmin, create a database named
`research_management`.

From the project root:

```powershell
Copy-Item .env.example .env
notepad .env
```

Set `DB_PASSWORD` to the password created during PostgreSQL installation. Do not
commit `.env` to Git.

Also set a session secret:

```env
APP_SECRET_KEY=replace_with_a_long_random_secret
APP_HOST=127.0.0.1
APP_PORT=8000
```

## 4 Create Tables and Admin User

```powershell
python scripts/init_database.py
```

Expected result:

```text
Database tables are ready.
Default login: admin / admin123
```

## 5 Start the Web Application

```powershell
python main.py
```

Or use:

```powershell
.\scripts\run_windows.ps1
```

Open this address in your browser:

```text
http://127.0.0.1:8000
```

Login with:

```text
Username: admin
Password: admin123
```

## 6 Load Demo Data

After logging in:

1. Select **Import** in the navigation bar.
2. Choose `data/sample_papers.csv`.
3. Return to **Library**.
4. Use the search box to find a title or author.
5. Use the sort link to switch chronological direction.
6. Open **Statistics**.

## 7 Run Tests

```powershell
pytest
ruff check .
```

## 8 Run the Legacy Desktop Interface

The previous desktop GUI can still be started with:

```powershell
python desktop_main.py
```

## 9 Run the Packaged Web Application

The web build is placed in `dist\ResearchPaperManager\`.
Before starting the executable, copy the configured `.env` file into
`dist\ResearchPaperManager\`, beside `ResearchPaperManager.exe`, and ensure
PostgreSQL is running. Start the executable, then open
`http://127.0.0.1:8000`.

For a release build made on the development laptop:

```powershell
python -m PyInstaller --noconfirm --clean --paths src --name ResearchPaperManager `
  --add-data "src/research_manager/web/templates;research_manager/web/templates" `
  --add-data "src/research_manager/web/static;research_manager/web/static" `
  main.py
```

The executable contains the Python and web runtime, but it does not contain
PostgreSQL or the database data.
