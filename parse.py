# TODO: This grammar does not provide for expressions as keys
# Can probably substitute KVMap for Atom in KVPair.
'''
Parsing transforms a stream of tokens into a stream of parse trees.

Grammar:
Expr = Atom |
       ( KVMap ) |
       [ ListMap ]

KVMap = KVPair KVMap | Empty

KVPair = Atom : Expr

ListMap = Expr ListMap | Empty
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
        try:
            yield match_expr(ts)
        except StopIteration:
            return


def match_expr(tokens):
    t = next(tokens)

    if t.name() == 'ATOM':
        return t.value()

    elif t.name() == 'LPAREN':
        match_lparen(t)
        m = match_kv_map(tokens)
        match_rparen(next(tokens))
        return m

    else:
        match_lsquare(t)
        m = match_list_map(tokens, 0)
        t = next(tokens)
        match_rsquare(t)
        return m


def match_lparen(token):
    if token.name() != 'LPAREN':
        print('Error: expected "("')
        raise StopIteration
    return None


def match_rparen(token):
    if token.name() != 'RPAREN':
        print('Error: expected ")"')
        raise StopIteration
    return None


def match_lsquare(token):
    if token.name() != 'LSQUARE':
        print('Error: expected "["')
        raise StopIteration
    return None


def match_rsquare(token):
    if token.name() != 'RSQUARE':
        print('Error: expected "]"')
        raise StopIteration
    return None


def match_kv_map(tokens):
    m = {}
    k, v = match_kv_pair(tokens)
    m[k] = v

    t = peek(tokens)
    if t.name() != 'RPAREN':
        m.update(match_kv_map(tokens))

    return m


def match_kv_pair(tokens):
    k = match_atom(next(tokens))
    match_colon(next(tokens))
    v = match_expr(tokens)
    return k, v


def match_list_map(tokens, i):
    m = {}
    v = match_expr(tokens)
    m[i] = v

    t = peek(tokens)
    if t.name() != 'RSQUARE':
        m.update(match_list_map(tokens, i+1))

    return m


def match_colon(token):
    if token.name() != 'COLON':
        print("Error: expected ':'")
        sys.exit(0)
    return None


def match_atom(token):
    if token.name() != 'ATOM':
        print('Error: expected atom')
        raise StopIteration
    return token.value()
