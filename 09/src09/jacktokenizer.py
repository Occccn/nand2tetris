from collections import deque


class JackAnalyzer:
    def __init__(self, path: str):
        with open(path) as f:
            self.lines = deque(f.readlines())

    def HasmoreTokens(self):
        pass

    def advance(self):
        pass

    def tokenType(self):
        pass

    def keyWord(self):
        pass

    def symbol(self):
        pass

    def identifier(self):
        pass

    def intVal(self):
        pass

    def stringVal(self):
        pass
