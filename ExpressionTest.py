import CompilationEngine as ce
a = ce.CompilationEngine("((y + size) < 254) & ((x + size) < 510)",'')
a.compileExpression()
print(a.outputString)
print(a.tk.tokenList)