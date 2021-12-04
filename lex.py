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


class LBRACKET(Token):
    def name(self):
        return "LBRACKET"

    def value(self):
        return "{"


class RBRACKET(Token):
    def name(self):
        return "RBRACKET"

    def value(self):
        return "}"


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


class RAISE(Token):
    def name(self):
        return "RAISE"

    def value(self):
        return "↑"


class COLLAPSE(Token):
    def name(self):
        return "COLLAPSE"

    def value(self):
        return "↓"


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

    # TODO: no reason this shouldn't be a set, right?
    reserved = ['(', ')', '[', ']', '{', '}', ':']

    c = cs.read(1)
    while c != '':
        if c == '"':
            n = c
            c = cs.read(1)
            while c != '"':
                n += c
                c = cs.read(1)
            n += c
            c = cs.read(1)
            yield ATOM(n)

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

        elif c == '{':
            c = cs.read(1)
            yield LBRACKET()

        elif c == '}':
            c = cs.read(1)
            yield RBRACKET()

        elif c == ':':
            c = cs.read(1)
            yield COLON()

        elif c == '↑':
            c = cs.read(1)
            yield RAISE()

        elif c == '↓':
            c = cs.read(1)
            yield COLLAPSE()

        else:
            n = cs.read(1)
            while n not in reserved and not n.isspace():
                c = c + n
                n = cs.read(1)
            yield ATOM(c)
            c = n
    return
