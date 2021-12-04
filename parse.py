# TODO: This grammar does not provide for expressions as keys
# Can probably substitute KVMap for Atom in KVPair.
'''
Parsing transforms a stream of tokens into a stream of parse trees.

Grammar:
Expr = Atom |
       ( KVMap ) |
       [ ListMap ]
       { SetMap }

KVMap = KVPair KVMap | Empty

KVPair = Atom : Expr

ListMap = Expr ListMap | Empty
'''
import sys

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


class TaliSet():
    '''
    We need to store a parsed set so that it can be evaluated at
    a later time (because we implement sets as hash maps where
    the key is the same as the value, and you can't use dict or
    sets as keys - we need to evaluate them first).
    '''

    def __init__(self, expressions):
        self.expressions = expressions


def match_expr(tokens):
    t = next(tokens)

    if t.name() == 'ATOM':
        return t.value()

    elif t.name() == 'LPAREN':
        match_lparen(t)

        # Handle the empty case 
        t = peek(tokens)
        if t.name() == 'RPAREN':
            match_rparen(next(tokens))
            return {}

        m = match_kv_map(tokens)
        match_rparen(next(tokens))
        return m

    elif t.name() == 'LSQUARE':
        match_lsquare(t)

        # Handle the empty case 
        t = peek(tokens)
        if t.name() == 'RSQUARE':
            match_rsquare(next(tokens))
            return {'len': '0'}

        m = match_list_map(tokens, 0)
        match_rsquare(next(tokens))
        return m

    else:
        match_lbracket(t)

        # Handle the empty case 
        t = peek(tokens)
        if t.name() == 'RBRACKET':
            match_rbracket(next(tokens))
            return TaliSet({})

        m = match_set_map(tokens, 0)
        match_rbracket(next(tokens))
        return TaliSet(m)


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


def match_lbracket(token):
    if token.name() != 'LBRACKET':
        print('Error: expected "{"')
        raise StopIteration
    return None


def match_rbracket(token):
    if token.name() != 'RBRACKET':
        print('Error: expected "}"')
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
        m.update(match_list_map(tokens, i + 1))

    m['len'] = len(m) - 1
    return m


def match_set_map(tokens, i):
    m = {}
    v = match_expr(tokens)
    m[i] = v

    t = peek(tokens)
    if t.name() != 'RBRACKET':
        m.update(match_set_map(tokens, i + 1))

    return m


# def match_set_map(tokens, i):
#     '''
#     This is tricky; the end-goal is to have a set of expressions,
#     such that we have constant-time access as to whether the value
#     is in the set.
# 
#     We don't know the value of an expression at parse time. That
#     means we need to store it somehow for evaluation later.
# 
#     For now, we'll treat it the same as a list, but evaluate
#     it differently in the interpreter.
#     '''
#     m = {}
#     v = match_expr(tokens)
#     m[i] = v
# 
#     t = peek(tokens)
#     if t.name() != 'RBRACKET':
#         m.update(match_list_map(tokens, i + 1))
# 
#     m['len'] = len(m)
#     return m


def match_colon(token):
    if token.name() != 'COLON':
        print("Error: expected ':'")
        raise StopIteration
    return None


def match_atom(token):
    if token.name() != 'ATOM':
        print('Error: expected atom')
        raise StopIteration
    return token.value()
