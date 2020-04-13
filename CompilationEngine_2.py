import JackTokenizer

class CompilationEngine:
    def __init__(self, inputString, outputFile):
        self.tk = JackTokenizer.JackTokenizer(inputString)
        self.outputString = ''
        self.outputFile = outputFile
        self.compClassDict = {'field':self.compileClassVarDec, 'static':self.compileClassVarDec, 'constructor':self.compileSubroutineDec, 
        'function':self.compileSubroutineDec, 'method':self.compileSubroutineDec}
        self.compStatementDict = {'let':self.compileLet, 'if':self.compileIf, 'while':self.compileWhile, 'do':self.compileDo, 'return':self.compileReturn}
        self.compTokenDict = {'symbol':self.tk.symbol, 'keyword':self.tk.keyword, 'identifier':self.tk.identifier, 'integerConstant':self.tk.intVal, 'stringConstant':self.tk.stringVal}
        self.XMLSymDict = {'<':'&lt;', '>':'&gt;', '&':'&amp;', '"':'&quot'}
        self.multiTermExpression = False
        self.indent = ''

    def compileClass(self): # 'class' className '{' classVarDec* subroutineDec* '}'
        #self.outputString += '<tokens>\n'
        
        #'class'
        self.outputString += self.indent + '<class>\n'
        self.addIndent()
        self.process('keyword', 'class')
        
        #className
        self.process('identifier', category='class')
        
        #'{'
        self.process('symbol', '{')
        self.tk.advance()
        
        while not (self.tk.tokenType() == 'symbol' and self.tk.symbol() == '}'):
            self.process('keyword', self.compClassDict.keys(), False, False)
            self.compClassDict[self.tk.keyword()]()

        #'}
        self.process('symbol', '}', False)
        self.removeIndent()
        self.outputString += self.indent + '</class>\n'
        #self.outputString += '</tokens>\n'
        print(self.outputString)

    def compileClassVarDec(self, advance=False): # ('static'|'field') type varName (',' varName )* ';'
        
        self.outputString += self.indent + '<classVarDec>\n'
        self.addIndent()
        
        #static or field
        self.process('keyword', ['field', 'static'], advance)
        
        #type declaration
        self.process(['keyword', 'identifier'], ['void', 'int', 'char', 'boolean'])
        
        #variable declarations
        while self.tk.symbol() != ';':
            self.process('identifier')
            self.process('symbol',[',', ';'])
        self.tk.advance()
        
        self.removeIndent()
        self.outputString += self.indent + '</classVarDec>\n'
        
    def compileSubroutineDec(self, advance=False): # ('constructor' | 'function' | 'method') ('void' | type) subroutineName '(' parameterList ')' subroutineBody
        self.outputString += self.indent + '<subroutineDec>\n'
        self.addIndent()

        #subroutine keyword
        self.process('keyword', ['constructor', 'function', 'method'], advance)

        #type declaration
        self.process(['keyword', 'identifier'], ['void', 'int', 'char', 'boolean'])
        
        #subroutineName
        self.process('identifier')
        
        # ( parameterList )
        self.process('symbol', '(')      
        self.compileParameterList()
        self.process('symbol', ')', advance=False)
        
        #subroutineBody
        self.compileSubroutineBody()
        
        self.removeIndent()
        self.outputString += self.indent + '</subroutineDec>\n'

    def compileParameterList(self):
        self.outputString += self. indent + '<parameterList>\n'
        self.addIndent()
        self.tk.advance()
        if self.tk.symbol() != ')':
            self.process(['keyword', 'identifier'], ['int', 'char', 'boolean'], advance=False)
            self.process('identifier')
            self.tk.advance()
            while not (self.tk.tokenType() == 'symbol' and self.tk.symbol() == ')'):
                self.process('symbol', ',', False)
                self.process(['keyword', 'identifier'], ['int', 'char', 'boolean'])
                self.process('identifier')
                self.tk.advance()
                
        self.removeIndent()
        self.outputString += self.indent + '</parameterList>\n'
        
    def compileSubroutineBody(self):
        self.outputString += self.indent + '<subroutineBody>\n'
        self.addIndent()
        
        self.process('symbol', '{')
        self.tk.advance()   
        while self.tk.tokenType() == 'keyword' and self.tk.keyword() == 'var':
            self.compileVarDec()
            self.tk.advance()
        self.compileStatements()
        self.process('symbol','}', advance=False)
        self.tk.advance()
        
        self.removeIndent()
        self.outputString += self.indent + '</subroutineBody>\n'        

    def compileVarDec(self):
        self.outputString += self.indent + '<varDec>\n'
        self.addIndent()
        
        self.process('keyword', 'var', advance=False)
        self.process(['keyword', 'identifier'], ['int', 'char', 'boolean'])
        while True:
            self.process('identifier')
            self.process('symbol', [',', ';'])
            if self.tk.tokenType() == 'symbol' and self.tk.symbol() == ';':
                break
                
        self.removeIndent()
        self.outputString += self.indent + '</varDec>\n'

    def compileStatements(self):
        self.outputString += self.indent + '<statements>\n'
        self.addIndent()
        
        while not (self.tk.tokenType() == 'symbol' and self.tk.symbol() == '}'):
            self.process('keyword', ['let', 'if', 'while', 'do', 'return'], False, False)
            self.compStatementDict[self.tk.keyword()]()
            
        self.removeIndent()
        self.outputString += self.indent + '</statements>\n'
    
    def compileLet(self):
        self.outputString += self.indent + '<letStatement>\n' + self.indent + '<keyword> let </keyword>\n'
        self.addIndent()
        
        self.process('identifier')
        self.process('symbol', ['=', '['])
        if self.tk.symbol() == '[':
            self.compileExpression()
            self.process('symbol', ']', advance=False)
            self.process('symbol', '=')
        self.compileExpression()
        self.process('symbol', ';', advance=False)
        self.tk.advance()
        
        self.removeIndent()
        self.outputString += self.indent + '</letStatement>\n'        

    def compileIf(self):
        self.outputString += self.indent + '<ifStatement>\n'
        self.addIndent()
        
        self.outputString += self.indent + '<keyword> if </keyword>\n'
        self.process('symbol', '(', advance=True)
        self.compileExpression()
        self.process('symbol', ')', advance=False)
        self.process('symbol', '{')
        self.tk.advance()
        self.compileStatements()
        self.process('symbol', '}',advance=False)
        self.tk.advance()
        self.checkType(['keyword','symbol'], 'expected an else or another statement')
        if self.tk.tokenType() == 'keyword' and self.tk.keyword() == 'else':
            self.outputString += self.indent + '<keyword> else </keyword>\n'
            self.process('symbol', '{')
            self.tk.advance()
            self.compileStatements()
            self.process('symbol', '}', advance=False)
            self.tk.advance()
            
        self.removeIndent()
        self.outputString += self.indent + '</ifStatement>\n'
        
    def compileWhile(self):
        self.outputString += self.indent + '<whileStatement>\n'
        self.addIndent()
        
        self.outputString += self.indent + '<keyword> while </keyword>\n'
        self.process('symbol', '(')
        self.compileExpression()
        self.process('symbol', ')', advance=False)
        self.process('symbol', '{')
        self.tk.advance()
        self.compileStatements()
        self.process('symbol', '}' , advance=False)
        self.tk.advance()
        
        self.removeIndent()
        self.outputString += self.indent + '</whileStatement>\n'

    def compileDo(self):
        self.outputString += self.indent + '<doStatement>\n'
        self.addIndent()
        
        self.process('keyword', 'do', advance=False)
        self.process('identifier', ' a class or subroutine name')
        self.process('symbol', ['(','.'])
        if self.tk.symbol() == '(':
            self.compileExpressionList()
        elif self.tk.symbol() == '.':
            self.process('identifier', 'a subroutine name')
            self.process('symbol', '(')
            self.compileExpressionList()
        self.process('symbol', ')', advance=False)
        self.process('symbol', ';')
        self.tk.advance()
        
        self.removeIndent()
        self.outputString += self.indent + '</doStatement>\n'

    def compileReturn(self):
        self.outputString += self.indent + '<returnStatement>\n'
        self.addIndent()
        
        self.process('keyword', 'return', advance=False)
        self.tk.advance()
        if not (self.tk.tokenType() == 'symbol' and self.tk.symbol() == ';'):
            self.compileExpression(False)
        self.process('symbol', ';', advance=False)
        self.tk.advance()
        
        self.removeIndent()
        self.outputString += self.indent + '</returnStatement>\n'        

    def compileExpression(self, advance=True):
        self.outputString += self.indent + '<expression>\n'
        self.addIndent()
        
        self.multiTermExpression = False
        self.compileTerm(advance)
        if self.tk.tokenType() == 'symbol' and self.tk.symbol() in ['+', '-', '*', '/', '&', '|', '<', '>', '=']:
            while True:
                self.multiTermExpression = True
                self.process('symbol', ['+', '-', '*', '/', '&', '|', '<', '>', '='], advance=False)
                self.compileTerm()
                if self.tk.symbol() not in ['+', '-', '*', '/', '&', '|', '<', '>', '=']:
                    break
                    
        self.removeIndent()
        self.outputString += self.indent + '</expression>\n'

    def compileTerm(self, advance=True):
        self.outputString += self.indent + '<term>\n'
        self.addIndent()
        
        self.process(['integerConstant', 'stringConstant', 'keyword', 'identifier', 'symbol'], ['true', 'false', 'null', 'this', '(', '-', '~'], advance)
        if self.tk.tokenType() == 'symbol' and self.tk.symbol() in ['-', '~']: #unaryOp term
            self.compileTerm()            
        elif self.tk.tokenType() == 'symbol' and self.tk.symbol() == '(': #(expression)
            self.compileExpression()
            self.process('symbol', ')', advance=False)
            self.tk.advance()
        else: self.tk.advance()
        if self.tk.tokenType() == 'symbol' and self.tk.symbol() in ['[', '(', '.']:
            if self.tk.symbol() == '[':
                self.process('symbol', '[', advance=False)
                self.compileExpression()
                self.process('symbol', ']', advance=False)
            elif self.tk.symbol() == '(':
                self.process('symbol', '(', advance=False)
                self.compileExpressionList()
                self.process('symbol', ')', advance=False)
            elif self.tk.symbol() == '.':
                self.process('symbol', '.', advance=False)
                self.process('identifier')
                self.process('symbol', '(')
                self.compileExpressionList()
                self.process('symbol', ')', advance=False)
            self.tk.advance()
            
        self.removeIndent()
        self.outputString += self.indent + '</term>\n'
        
    def compileExpressionList(self):
        self.outputString += self.indent + '<expressionList>\n'
        self.addIndent()
        
        self.tk.advance()
        if self.tk.symbol() != ')':
            self.compileExpression(False)
            while self.tk.symbol() == ',':
                self.process('symbol', ',', advance=False)
                self.compileExpression()
            #self.tk.advance()
            
        self.removeIndent()
        self.outputString += self.indent + '</expressionList>\n'

    def checkToken(self, token, expectedTokens, message = ''):
        if token not in expectedTokens:
            raise ValueError(message)
        else:
            pass
    
    def checkType(self, expectedTypes, message):
        if self.tk.tokenType() not in expectedTypes:
            print(self.outputString)
            raise TypeError(message)
        else:
            pass
            
    def addIndent(self):
        self.indent += '  '
        
    def removeIndent(self):
        self.indent = self.indent[:len(self.indent)-2]

    def process(self, expectedTypes, expectedTokens='', category = None, advance=True, xmlOut = True):
        xmlAttr = ''
        if advance:
            self.tk.advance()
        self.checkType(expectedTypes, 'Expected '+' or '.join(expectedTypes) + ', got ' + self.tk.tokenType() + ' instead' if isinstance(expectedTypes, list) else 'Expected '+ expectedTypes + ', got ' + self.tk.tokenType() + ' instead')
        token = self.compTokenDict[self.tk.tokenType()]()
        if self.tk.tokenType() in ['symbol', 'keyword']:
            self.checkToken(token, expectedTokens, 'Expected '+' or '.join(expectedTokens) + ', got ' + self.tk.currentToken + ' instead')
        elif self.tk.tokenType() == 'identifier':
            xmlAttr = ' category=' + self.tk.previousToken()
        if xmlOut:
            if self.tk.symbol() in self.XMLSymDict:
                self.outputString += self.indent + '<'+self.tk.tokenType()+ xmlAttr +'>'+self.XMLSymDict[token]+'</'+self.tk.tokenType()+'>\n'
            else:
                self.outputString += self.indent + '<'+self.tk.tokenType()+ xmlAttr + '>'+token+'</'+self.tk.tokenType()+'>\n'

    def writeOutput(self):
        open(self.outputFile, 'w').write(self.outputString)
        