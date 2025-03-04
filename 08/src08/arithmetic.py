import dataclasses
from typing import List


@dataclasses.dataclass(frozen=True)
class Arithmetic:
    arithmetic: List[str] = dataclasses.field(default_factory=lambda: ["add", "sub", "neg"])
    comparison: List[str] = dataclasses.field(default_factory=lambda: ["eq", "gt", "lt"])
    logical: List[str] = dataclasses.field(default_factory=lambda: ["and", "or", "not"])
