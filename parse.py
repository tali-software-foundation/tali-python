'''
Parsing transforms a stream of tokens into a stream of parse trees.

Grammar:
Expr = Atom |
       ( KVList )

KVList = KVPair , KVList | Empty

KVPair = Atom: Expr
'''
import sys

namespaces = {}

class Peekable:
    '''
    Utility class to facilitate LL(1) parsing, as Python
    generators don't have any lookahead.
    '''
    def __init__(self, iterable):
        self.iterable = iter(iterable)
        self.buffer = []

    def __iter__(self):
        return self

    def __next__(self):
        if self.buffer:
            return self.buffer.pop(0)
        else:
            return next(self.iterable)

    def peek(self):
        """
        Peek at the next iterable and buffer it in.
        """
        try:
            self.buffer.append(next(self.iterable))
        except StopIteration:
            return None

        return self.buffer[0]


def peek(peekable):
    return peekable.peek()


def parse(tokens):
    '''
    Transforms a stream of tokens in a stream of parse trees.
    The parameter 'tokens' should be an iterable.
    '''
    # No need for try/except: we'd just re-throw
    ts = Peekable(tokens)
    while True:
        print(match_expr(ts))


def match_expr(tokens):
    t = next(tokens)

    if t.name() == 'ATOM':
        return ('ATOM', t.value())
    else:
        children = []
        children.append(match_lparen(t))
        children.append(match_kv_list(tokens))
        children.append(match_rparen(next(tokens)))
        return ('EXPR', children)


def match_lparen(token):
    if token.name() != 'LPAREN':
        print('Error: expected "("')
        raise StopIteration
    return '('


def match_rparen(token):
    if token.name() != 'RPAREN':
        print('Error: expected ")"')
        raise StopIteration
    return ')'


def match_kv_list(tokens):
    children = []
    children.append(match_kv_pair(tokens))

    t = peek(tokens)
    if t.name() == 'COMMA':
        children.append(next(tokens))
        children.append(match_kv_list(tokens))

    return ('KVL', children)

 
def match_kv_pair(tokens):
    children = []
    children.append(match_atom(next(tokens)))
    children.append(match_colon(next(tokens)))
    children.append(match_expr(tokens))
    return ('KVP', children)


def match_colon(token):
    if token.name() != 'COLON':
        print("Error: expected ':'")
        sys.exit(0)
    return ':'


def match_atom(token):
    if token.name() != 'ATOM':
        print('Error: expected atom')
        raise StopIteration
    return ('ATOM', token.value())
