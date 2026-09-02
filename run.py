import subprocess
import sys
from pathlib import Path


project_dir = Path(__file__).parent
requirements_file = project_dir / "requirements.txt"
game_file = project_dir / "dice.py"

subprocess.check_call(
    [sys.executable, "-m", "pip", "install", "-q", "-r", str(requirements_file)]
)
subprocess.check_call([sys.executable, str(game_file)])
