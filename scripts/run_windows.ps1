Set-Location (Split-Path -Parent $PSScriptRoot)

if (-not (Test-Path ".venv\Scripts\python.exe")) {
    Write-Error "Virtual environment not found. Run: python -m venv .venv"
    exit 1
}

& ".venv\Scripts\python.exe" "main.py"
