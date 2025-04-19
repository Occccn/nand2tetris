from typing import Literal


class VMWriter:
    def __init__(self, output_file) -> None:
        self.f = open(output_file, "w")

    def write_push(
        self,
        segment: Literal["CONSTANT", "ARGUMENT", "LOCAL", "STATIC", "THIS", "THAT", "POINTER", "TEMP"],
        index: int,
    ) -> None:
        pass

    def write_pop(
        self, segment: Literal["ARGUMENT", "LOCAL", "STATIC", "THIS", "THAT", "POINTER", "TEMP"], index: int
    ) -> None:
        pass

    def write_arithmetic(self, command: Literal["ADD", "SUB", "NEG", "EQ", "GT", "LT", "AND", "OR", "NOT"]) -> None:
        pass

    def write_label(self, label: str) -> None:
        pass

    def write_goto(self, label: str) -> None:
        pass

    def write_if(self, label: str) -> None:
        pass

    def write_call(self, name: str, n_args: int) -> None:
        pass

    def write_function(self, name: str, n_locals: int) -> None:
        pass

    def write_return(self) -> None:
        pass

    def close(self) -> None:
        self.f.close()
