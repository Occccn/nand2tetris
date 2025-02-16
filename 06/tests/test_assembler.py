import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).parents[1]


def test_all_asm():
    files = ["Add.asm", "Max.asm", "MaxL.asm", "Pong.asm", "PongL.asm", "Rect.asm", "RectL.asm"]
    for file in files:
        print("testing", file)
        subprocess.run(["python", BASE_DIR / "src06/assembler.py", "-f", file])
        output_str = subprocess.run(
            ["diff", BASE_DIR / f"outputs/{file.split('.')[0]}.hack", BASE_DIR / f"answer/{file.split('.')[0]}.hack"],
            capture_output=True,
            text=True,
        ).stdout
        assert output_str != ""
