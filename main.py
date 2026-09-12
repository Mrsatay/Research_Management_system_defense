import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from research_manager.web.app import run_server

if __name__ == "__main__":
    run_server()
