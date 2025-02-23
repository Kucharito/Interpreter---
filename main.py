class Token:
    def __init__(self,type,value):
        self.type=type
        self.value=value

    def __str__(self):
        return "Token({type},{value})".format(type=self.type,value=repr(self.value))

class Lexer:
    def __init__(self,text):
        self.text=text
        self.pos=0
        self.current_char=self.text[self.pos]

    def advance(self):
        """presun na dalsi znak"""
        self.pos=self.pos+1
        if self.pos>len(self.text)-1:
            self.current_char=None
        else:
            self.current_char=self.text[self.pos]

    def skip_whitespace(self):
        """preskoc medzru"""
        while self.current_char and self.current_char.isspace():
            self.advance()

    def isDigit(self):
        """ak je znak cislo return"""
        digits = []
        while self.current_char and self.current_char.isdigit():
            digits.append(self.current_char)
            self.advance()
        return int(''.join(digits))

    def get_token(self):
        """analyzuj text a vrat Token"""
        while self.current_char:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            if self.current_char.isdigit():
                return Token('INTEGER', self.isDigit())
            if self.current_char=="+":
                self.advance()
                return Token('PLUS', "+")
            if self.current_char=="-":
                self.advance()
                return Token('MINUS',"-")
            if self.current_char=="*":
                self.advance()
                return Token('MUL',"*")
            if self.current_char=="/":
                self.advance()
                return Token('DIV',"/")
            if self.current_char=="(":
                self.advance()
                return Token('LPAREN',"(")
            if self.current_char==")":
                self.advance()
                return Token('RPAREN',")")

            self.error()
        return Token('EOF',None)

class Parser:
    def __init__(self,lexer):
        self.lexer=lexer
        self.current_token=self.lexer.get_token()

    def advance(self,token_type):
        if self.current_token.type==token_type:
            self.current_token=self.lexer.get_token()
        else:
            raise Exception("Error")

    def factor(self):
        """spracovanie cisla / vyrazu v zatvorkach"""
        token=self.current_token
        if token.type=='INTEGER':
            self.advance('INTEGER')
            return token.value
        elif token.type=='LPAREN':
            self.advance('LPAREN')
            result = self.expr()
            self.advance('RPAREN')
            return result
        else:
            raise Exception("Error")

    def term(self):
        """spracovanie nasobenia a delenia"""
        result=self.factor()
        while self.current_token.type in('MUL', 'DIV'):
            token=self.current_token
            if token.type=='MUL':
                self.advance('MUL')
                result=result*self.factor()
            elif token.type=='DIV':
                self.advance('DIV')
                result=result/self.factor()
            else:
                raise Exception("Error")
        return result

    def expr(self):
        result=self.term()
        while self.current_token.type in ('PLUS','MINUS'):
            token=self.current_token
            if token.type=='PLUS':
                self.advance('PLUS')
                result=result+self.term()
            elif token.type=='MINUS':
                self.advance('MINUS')
                result=result-self.term()
            else:
                raise Exception("Error")
        return result

    def parse(self):
        return self.expr()

def main():
    try:
        n=int(input())
        for i in range(n):
            text=input()
            lexer=Lexer(text)
            parser=Parser(lexer)
            try:
                result=parser.parse()
                print("vysledok je:", result)
            except Exception:
                print("ERROR")
    except ValueError:
        print("invalid number entered")

if __name__=="__main__":
    main()




