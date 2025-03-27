class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value


class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def advance(self):
        """posun na dalsi znak"""
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

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

    def error(self):
        raise Exception("Error parsing input")

    def skip_comment(self):
        while self.current_char and self.current_char != "\n":
            self.advance()
        self.advance()

    def isIdentifier(self):
        """ak je znak pismeno return"""
        identifier = []
        while self.current_char and self.current_char.isalpha():
            identifier.append(self.current_char)
            self.advance()
        return ''.join(identifier)

    def get_token(self):
        """analyzuj text a vrat Token"""
        while self.current_char:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            if self.current_char.isdigit():
                return Token('NUM', self.isDigit())
            if self.current_char == "+":
                self.advance()
                return Token('OP', "+")
            if self.current_char == "-":
                self.advance()
                return Token('OP', "-")
            if self.current_char == "*":
                self.advance()
                return Token('OP', "*")
            if self.current_char == "/" and self.text[self.pos:self.pos + 1] != "/":
                self.advance()
                return Token('OP', "/")
            if self.current_char == "(":
                self.advance()
                return Token('LPAR', "(")
            if self.current_char == ")":
                self.advance()
                return Token('RPAR', ")")
            if self.text[self.pos:self.pos + 3] == "mod":
                self.pos = self.pos + 3
                self.current_char = self.text[self.pos] if self.pos < len(self.text) else None
                return Token('MOD', "mod")
            if self.text[self.pos:self.pos + 3] == "div":
                self.pos = self.pos + 3
                self.current_char = self.text[self.pos] if self.pos < len(self.text) else None
                return Token('DIV', "div")
            if self.current_char == ";":
                self.advance()
                return Token('SEMICOLON', ";")
            if self.text[self.pos:self.pos + 2] == "//":
                self.skip_comment()
                continue

            if self.current_char.isalpha():
                identifier = self.isIdentifier()
                return Token('ID', identifier)
            self.error()
        return Token('EOF', None)


lexer = Lexer("    -2 + (245 div 3);  // note\n 2 mod 3 * hello")
token = lexer.get_token()
while token.type != 'EOF':
    print(f"{token.type}: {token.value}")
    token = lexer.get_token()
