class SymbolTable:
    def __init__(self) -> None:
        self.table: dict[str, int] = {}

    def addEntry(self, symbol: str, address: int) -> None:
        self.table[symbol] = address

    def contains(self, symbol: str) -> bool:
        return symbol in self.table

    def getAddress(self, symbol: str) -> int:
        return self.table[symbol]
