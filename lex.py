'''
Lexical analysis transforms a stream of characters into a stream
of tokens.
'''

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


class LSQUARE(Token):
    def name(self):
        return "LSQUARE"

    def value(self):
        return "["


class RSQUARE(Token):
    def name(self):
        return "RSQUARE"

    def value(self):
        return "]"


class COLON(Token):
    def name(self):
        return "COLON"

    def value(self):
        return ":"


class ATOM(Token):
    def __init__(self, val):
        self.val = val

    def name(self):
        return "ATOM"

    def value(self):
        return self.val


def tokenize(cs):
    '''
    Given a character stream (file), yield a stream of tokens.
    '''
    reserved = ['(', ')', '[', ']', ':']

    c = cs.read(1)
    while c != '':
        if c.isspace():
            c = cs.read(1)

        elif c == '(':
            c = cs.read(1)
            yield LPAREN()

        elif c == ')':
            c = cs.read(1)
            yield RPAREN()

        elif c == '[':
            c = cs.read(1)
            yield LSQUARE()

        elif c == ']':
            c = cs.read(1)
            yield RSQUARE()

        elif c == ':':
            c = cs.read(1)
            yield COLON()

        else:
            n = cs.read(1)
            while n not in reserved and not n.isspace():
                c = c + n
                n = cs.read(1)
            yield ATOM(c)
            c = n
    return
