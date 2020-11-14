'''
Lexical analysis transforms a stream of characters into a stream
of tokens.
'''

import io

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


def tokenize(cs):
    '''
    Given a character stream (file), yield a stream of tokens.
    '''
    c = cs.read(1)
    while c != '':
        if c.isspace():
            c = cs.read(1)
            continue

        reserved = ['(', ')', ':', ',']

        if c == '(':
            c = cs.read(1)
            yield LPAREN()

        elif c == ')':
            c = cs.read(1)
            yield RPAREN()

        elif c == ':':
            c = cs.read(1)
            yield COLON()

        elif c == ',':
            c = cs.read(1)
            yield COMMA()

        else:
            n = cs.read(1)
            while n not in reserved:
                c = c + n
                cs.read(1)
            yield ATOM(c)
            c = n

    return
