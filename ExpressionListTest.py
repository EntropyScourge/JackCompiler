import CompilationEngine as ce
#a = ce.CompilationEngine('((size) < 254) & ((x) < 510)','')#,y+stuff,x+stuff -4 + moarstuff','')
a = ce.CompilationEngine('anotherClass.evenMoarStuff(y + size), meaninglessFunction(), ((y + size) < 254) & ((x + size) < 510), y+stuff[0], x+stuff[8] -4 + moarstuff, anotherClass.evenMoarStuff(x + 3), (-q), lol;','')
#a = ce.CompilationEngine('let x = thing.lol(lollo, 1, 3);', '')
try:
    a.compileExpressionList()
except:
    print(a.outputString)
#a.tk.advance()
#a.compileLet()
print(a.outputString)
print(a.tk.tokenList)