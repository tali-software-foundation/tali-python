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


class EOF(Token):
    def name(self):
        return "EOF"

    def value(self):
        return ""


def tokenize(stream):
    '''
    Given an IO stream, yield a stream of tokens.
    '''
    s = stream.read(1)
    while s != '':
        if s.isspace():
            s = stream.read(1)
            continue

        reserved = ['(', ')', ':', ',']

        if s == '(':
            yield LPAREN()

        elif s == ')':
            yield RPAREN()

        elif s == ':':
            yield COLON()

        elif s == ',':
            yield COMMA()

        else:
            n = stream.read(1)
            while n not in reserved:
                s = s + n
                n = stream.read(1)

            yield ATOM(s)

        s = stream.read(1)

    yield EOF()
    return
