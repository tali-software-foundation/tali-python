class Token():
    def name(self):
        return None

    def value(self):
        return None

    def __repr__(self):
        return f'({self.name()}, "{self.value()}")'


class LPAREN(Token):
    def name(self):
        return "LPAREN"

    def value(self):
        return "("


class RPAREN(Token):
    def name(self):
        return "RPAREN"

    def value(self):
        return ")"


class COLON(Token):
    def name(self):
        return "COLON"

    def value(self):
        return ":"


class COMMA(Token):
    def name(self):
        return "COMMA"

    def value(self):
        return ","


class ATOM(Token):
    def __init__(self, val):
        self.val = val

    def name(self):
        return "ATOM"

    def value(self):
        return self.val


def tokenize(program):
    # Remove all whitespace
    program = ''.join(program.split())

    tokens = []
    s = ''

    while len(program) > 0:
        s = program[0]
        program = program[1:]

        reserved = ['(', ')', ':', ',']

        if s == '(':
            tokens.append(LPAREN())

        elif s == ')':
            tokens.append(RPAREN())

        elif s == ':':
            tokens.append(COLON())

        elif s == ',':
            tokens.append(COMMA())

        else:
            n = program[0]
            while n not in reserved:
                s = s + n
                program = program[1:]
                n = program[0]

            tokens.append(ATOM(s))

    return tokens
