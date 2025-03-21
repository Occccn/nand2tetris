from src10.jackanalyzer import JackAnalyzer


class CompilationEngine:
    def __init__(self, input_file, output_file):
        self.jackanalyzer = JackAnalyzer(input_file)
        self.jackanalyzer.get_tokens()
        self.jackanalyzer.advance()
        self.jackanalyzer.tokenType()
        self.f = open(output_file, "w")

    def run(self):
        self.compileClass()
        self.f.close()

    def compileClass(self):
        pass

    def compileClassVarDec(self):
        pass

    def compileSubroutine(self):
        pass

    def compileParameterList(self):
        pass

    def compileVarDec(self):
        pass

    def compileStatements(self):
        pass

    def compileDo(self):
        pass

    def compileLet(self):
        pass

    def compileWhile(self):
        pass

    def compileReturn(self):
        pass

    def compileIf(self):
        pass

    def compileExpression(self):
        pass

    def compileTerm(self):
        pass

    def compileExpressionList(self):
        pass
