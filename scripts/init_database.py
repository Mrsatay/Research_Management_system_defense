import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from research_manager.database import initialize_database
from research_manager.services.auth_service import AuthService

if __name__ == "__main__":
    initialize_database()
    AuthService().ensure_default_admin()
    print("Database tables are ready.")
    print("Default login: admin / admin123")
