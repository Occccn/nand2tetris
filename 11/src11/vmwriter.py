from typing import Literal


class VMWriter:
    def __init__(self, output_file) -> None:
        self.f = open(output_file, "w")

    def write_push(
        self,
        segment: Literal["CONSTANT", "ARGUMENT", "LOCAL", "STATIC", "THIS", "THAT", "POINTER", "TEMP"],
        index: int,
    ) -> None:
        self.f.write(f"push {segment.lower()} {index}\n")

    def write_pop(
        self, segment: Literal["ARGUMENT", "LOCAL", "STATIC", "THIS", "THAT", "POINTER", "TEMP"], index: int
    ) -> None:
        self.f.write(f"pop {segment.lower()} {index}\n")

    def write_arithmetic(self, command: Literal["ADD", "SUB", "NEG", "EQ", "GT", "LT", "AND", "OR", "NOT"]) -> None:
        self.f.write(f"{command.lower()}\n")

    def write_label(self, label: str) -> None:
        self.f.write(f"label {label}\n")

    def write_goto(self, label: str) -> None:
        self.f.write(f"goto {label}\n")

    def write_if(self, label: str) -> None:
        self.f.write(f"if-goto {label}\n")

    def write_call(self, name: str, n_args: int) -> None:
        self.f.write(f"call {name} {n_args}\n")

    def write_function(self, name: str, n_locals: int) -> None:
        self.f.write(f"function {name} {n_locals}\n")

    def write_return(self) -> None:
        self.f.write("return\n")

    def write_char(self, char: str) -> None:
        self.f.write(f"push constant {ord(char)}\n")
        self.f.write("call String.appendChar 2\n")

    def close(self) -> None:
        self.f.close()
