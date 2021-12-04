'''
Parsing transforms a stream of tokens into a stream of parse trees.

Grammar:
Prod = Meta Prod | Expr

Expr = Atom |
       ( KVMap ) |
       [ ListMap ] |
       { SetMap }

KVMap = KVPair KVMap | Empty

KVPair = Prod : Prod

ListMap = Prod ListMap | Empty

SetMap = Prod SetMap | Empty
'''
import sys


class ProdA():
    """
    First production constructor.
    """
    def __init__(self, meta, prod):
        self.meta = meta
        self.prod = prod

    def __str__(self):
        return "\n".join([
            "ProdA",
            "\n".join(["  " + x for x in str(self.meta).split("\n")]),
            "\n".join(["  " + x for x in str(self.prod).split("\n")])
        ])


class ProdB():
    """
    Second production constructor.
    """
    def __init__(self, expr):
        self.expr = expr

    def __str__(self):
        return "\n".join([
            "ProdB",
            "\n".join(["  " + x for x in str(self.expr).split("\n")])
        ])


class ExprA():
    """
    First expression constructor, representing an atom.
    """
    def __init__(self, atom):
        self.atom = atom

    def __str__(self):
        return "\n".join([
            "ExprA",
            "\n".join(["  " + x for x in str(self.atom).split("\n")])
        ])


class ExprB():
    """
    Second expression constructor, representing a map.
    """
    def __init__(self, kv_map):
        self.kv_map = kv_map

    def __str__(self):
        return "\n".join([
            "ExprB",
            "\n".join(["  " + x for x in str(self.kv_map).split("\n")])
        ])


class ExprC():
    """
    Third expression constructor, representing a list.
    """
    def __init__(self, list_map):
        self.list_map = list_map

    def __str__(self):
        return "\n".join([
            "ExprC",
            "\n".join(["  " + x for x in str(self.list_map).split("\n")])
        ])


class ExprD():
    """
    Fourth expression constructor, representing a set.
    """
    def __init__(self, set_map):
        self.set_map = set_map

    def __str__(self):
        return "\n".join([
            "ExprD",
            "\n".join(["  " + x for x in str(self.set_map).split("\n")])
        ])


class Atom():
    def __init__(self, symbol):
        self.symbol = symbol

    def __str__(self):
        return "\n".join([
            "Atom",
            "\n".join(["  " + x for x in str(self.symbol).split("\n")])
        ])

class KVPair():
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __str__(self):
        return "\n".join([
            "KVPair",
            "\n".join(["  " + x for x in str(self.key).split("\n")]),
            "\n".join(["  " + x for x in str(self.value).split("\n")])
        ])


class KVMapA():
    def __init__(self, pair, kv_map):
        self.pair = pair
        self.kv_map = kv_map

    def __str__(self):
        return "\n".join([
            "KVMap",
            "\n".join(["  " + x for x in str(self.pair).split("\n")]),
            "\n".join(["  " + x for x in str(self.kv_map).split("\n")])
        ])


class KVMapB():
    '''
    Second KVMap constructor, representing the empty list.
    '''
    def __init__(self):
        pass

    def __str__(self):
        return ""


class ListMapA():
    def __init__(self, expr, list_map):
        self.expr = expr
        self.list_map = list_map

    def __str__(self):
        return "\n".join([
            "ListMapA",
            "\n".join(["  " + x for x in str(self.expr).split("\n")]),
            "\n".join(["  " + x for x in str(self.list_map).split("\n")])
        ])


class ListMapB():
    '''
    Second ListMap constructor, representing the empty list.
    '''
    def __init__(self):
        pass

    def __str__(self):
        return ""


class SetMapA():
    '''
    We need to store a parsed set so that it can be evaluated at
    a later time (because we implement sets as hash maps where
    the key is the same as the value, and you can't use dict or
    sets as keys - we need to evaluate them first).
    '''

    def __init__(self, expr, set_map):
        self.expr = expr
        self.set_map = set_map

    def __str__(self):
        return "\n".join([
            "SetMapA",
            "\n".join(["  " + x for x in str(self.expr).split("\n")]),
            "\n".join(["  " + x for x in str(self.set_map).split("\n")])
        ])


class SetMapB():
    '''
    Second SetMap constructor, representing the empty list.
    '''
    def __init__(self):
        pass

    def __str__(self):
        return ""


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
        # TODO: eliminate try/catch here, and line 185?
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
            yield match_prod(ts)
        except StopIteration:
            return


def match_prod(tokens):
    t = peek(tokens)
    if t is None: raise StopIteration
    if t.name() in ['RAISE', 'COLLAPSE']:
        next(tokens)
        return ProdA(t.value(), match_prod(tokens))
    return ProdB(match_expr(tokens))


def match_expr(tokens):
    t = next(tokens)

    if t.name() == 'ATOM':
        return ExprA(Atom(t.value()))

    elif t.name() == 'LPAREN':
        match_lparen(t)

        # Handle the empty case 
        t = peek(tokens)
        if t.name() == 'RPAREN':
            match_rparen(next(tokens))
            return ExprB(KVMapB())

        m = match_kv_map(tokens)
        match_rparen(next(tokens))
        return ExprB(m)

    elif t.name() == 'LSQUARE':
        match_lsquare(t)

        # Handle the empty case 
        t = peek(tokens)
        if t.name() == 'RSQUARE':
            match_rsquare(next(tokens))
            return ExprC(ListMapB())

        m = match_list_map(tokens)
        match_rsquare(next(tokens))
        return ExprC(m)

    else:
        match_lbracket(t)

        # Handle the empty case 
        t = peek(tokens)
        if t.name() == 'RBRACKET':
            match_rbracket(next(tokens))
            return ExprD(SetMapB)

        m = match_set_map(tokens)
        match_rbracket(next(tokens))
        return ExprD(m)


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
    pair = match_kv_pair(tokens)
    t = peek(tokens)
    if t.name() != 'RPAREN':
        return KVMapA(pair, match_kv_map(tokens))
    return KVMapA(pair, KVMapB())


def match_kv_pair(tokens):
    k = match_prod(tokens)
    match_colon(next(tokens))
    v = match_prod(tokens)
    return KVPair(k, v)


def match_list_map(tokens):
    v = match_prod(tokens)
    t = peek(tokens)
    if t.name() != 'RSQUARE':
        return ListMapA(v, match_list_map(tokens))
    return ListMapA(v, ListMapB())


def match_set_map(tokens, i):
    v = match_prod(tokens)
    t = peek(tokens)
    if t.name() != 'RBRACKET':
        return SetMapA(v, match_list_map(tokens))
    return SetMapA(v, SetMapB())


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
