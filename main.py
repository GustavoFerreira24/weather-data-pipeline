import subprocess
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent

steps = [
    ("Extract", "src/extract.py"),
    ("Transform and Load", "src/load.py"),
    ("SQL Analytics", "analysis/run_queries.py")
]

for name, script in steps:
    print(f"\nRunning {name}...", flush=True)

    subprocess.run(
        [sys.executable, script],
        cwd=project_root,
        check=True
    )