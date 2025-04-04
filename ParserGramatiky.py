class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current_token(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else (None, None)

    def match(self, expected_type):
        token_type, token_val = self.current_token()
        if token_type == expected_type:
            self.pos += 1
            return token_val
        else:
            raise SyntaxError(f"Očekáván '{expected_type}', ale nalezen '{token_type}'")

    def parse_E(self):
        f_val = self.parse_F()
        return self.parse_E1(f_val)

    def parse_E1(self, inherited):
        token_type, _ = self.current_token()
        if token_type == '+':
            self.match('+')
            f_val = self.parse_F()
            return self.parse_E1(inherited + f_val)
        elif token_type == '-':
            self.match('-')
            f_val = self.parse_F()
            return self.parse_E1(inherited - f_val)
        elif token_type == '*':
            self.match('*')
            f_val = self.parse_F()
            return self.parse_E1(inherited * f_val)
        elif token_type == '/':
            self.match('/')
            f_val = self.parse_F()
            return self.parse_E1(inherited / f_val)
        else:
            return inherited


    def parse_F(self):
        token_type, token_val = self.current_token()
        if token_type == 'num':
            self.match('num')
            return token_val
        elif token_type == '(':
            self.match('(')
            val = self.parse_E()
            self.match(')')
            return val
        else:
            raise SyntaxError(f"Neočekávaný token: {token_type}")

    def parse(self):
        result = self.parse_E()
        if self.pos != len(self.tokens):
            raise SyntaxError("Nezpracované tokeny na vstupu!")
        return result

# Test
tokens = [('num', 1), ('/', None), ('num', 2), ('*', None), ('(', None), ('num', 3), ('*', None), ('num', 4), (')', None)]
parser = Parser(tokens)
print("Výsledek:", parser.parse())