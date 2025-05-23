import argparse
from pathlib import Path

from src11.compilation_engine import CompilationEngine

BASE_DIR = Path(__file__).resolve().parents[1]


def main(dir_name: str) -> None:
    jack_files = list(BASE_DIR.glob(f"jack/{dir_name}/*.jack"))
    for jack_file in jack_files:
        output_file = jack_file.with_suffix(".xml")
        file_name = output_file.name.replace(output_file.name.split(".")[0], output_file.name.split(".")[0] + "Test")
        output_file = output_file.with_name(file_name)
        compilation_engine = CompilationEngine(jack_file, output_file)
        compilation_engine.run()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="JackAnalyzer for nand2tetris")
    parser.add_argument("-d", "--dir", help="dir name to jack", required=True)
    args = parser.parse_args()
    main(args.dir)
