import re
import sys
from decimal import Decimal
from inspect import isfunction

from lex import tokenize
from parse import parse

class Symbol(str): pass

class Namespace(dict):
    '''
    A namespace is a dictionary of (symbol, definition) pairs,
    with an optional parent namespace.
    '''
    def __init__(self, d, p=None):
        self.p = p
        self.update(d)

    def find(self, s):
        '''
        Find the innermost namespace in which a given symbol
        is defined.
        '''
        if s in self: return self
        elif self.p is None: raise LookupError(s)
        else: return self.p.find(s)


class Procedure(object):
    '''
    An instance of a Tali procedure, consisting of
    parameters, expression, and namespace.
    '''
    def __init__(self, ks, e, n):
        self.ks, self.e, self.n = ks, e, n

    def __call__(self, *vs):
        return eval(self.e, Namespace(ks, vs, self.n))


namespaces = {}
current = 'core'

# TODO: finish
def define(n, p, f, ns=current, nss=namespaces):
    '''
    Given a function name, parameters, and body, as well
    as a namespace and a namespace collection, define
    the respective function within the namespace within
    the collection.
    '''
    nss[ns][n] = {
        'p': p,
        'f': f
    }


def bind(k, v, ns=current, nss=namespaces):
    nss[ns][k] = v
    return v


def index(k, ns=current, nss=namespaces):
    return nss[ns][k]


def add(a, b):
    return a + b


def sub(a, b):
    return a - b


def mul(a, b):
    return a * b


def floordiv(a, b):
    return a // b


def truediv(a, b):
    return a / b


def gt(a, b):
    return a > b


def lt(a, b):
    return a < b


def gte(a, b):
    return a >= b


def lte(a, b):
    return a <= b


def eq(a, b):
    return a == b


# TODO: Want to be able to declare some namespaces immutable
# TODO: Want to return this value as a function
core = Namespace({
        'def': {
            'p': ['n', 'p', 'f'],
            'f': define
        },
        'bnd': {
            'p': ['k', 'p', 'f'],
            'f': bind
        },
        'idx': {
            'p': ['n', 'p', 'f'],
            'f': bind
        },
        '+': {
            'p': ['a', 'b'],
            'f': add
        },
        '-': {
            'p': ['a', 'b'],
            'f': sub
        },
        '*': {
            'p': ['a', 'b'],
            'f': mul
        },
        '//': {
            'p': ['a', 'b'],
            'f': floordiv
        },
        '/': {
            'p': ['a', 'b'],
            'f': truediv
        },
        '>': {
            'p': ['a', 'b'],
            'f': gt
        },
        '<': {
            'p': ['a', 'b'],
            'f': lt
        },
        '>=': {
            'p': ['a', 'b'],
            'f': gte
        },
        '<=': {
            'p': ['a', 'b'],
            'f': lte
        },
        '=': {
            'p': ['a', 'b'],
            'f': eq
        }
    })

# TODO: This construction should be returned via a function
# rather than sitting here, so that I can grab them and
# call eval in other contexts as well
namespaces['core'] = core

isa = isinstance

# TODO: Make tail-recursive
def eval(t, ns=current, nss=namespaces):
    '''
    Tail-recursive evaluation of an parse tree in a given
    environment.
    '''
    while True:
        # atom 
        if not isa(t, dict):
            if re.match('[0-9]+', t):
                return int(t)

            elif re.match('[0-9]+\.[0-9]+', t):
                return Decimal(t)

            elif re.match('\"\S\"', t):
                return str(t[1:-1])
            else:
                return nss[ns].find(t)[t]

        # Auto-quoted dictionary
        elif '@' not in t:
            return t

        # TODO: if q is an atom, then this is really
        # returning a string. The distinction should be
        # enforced more strongly to prevent this being
        # abused.
        elif t['@'] == 'quote':
            return t['q']

        # (@: if
        #  p: ...
        #  t: ...
        #  f: ...)
        elif t['@'] == 'if':
            pre = t['p']
            con = t['t']
            alt = t['f']
            t = con if eval(pre, ns, nss) else alt

        # (@: ...)
        else:
            d = nss[ns][t['@']]

            args = {}
            for p in d['p']:
                print(p)    # n
                print(t[p]) # add3
                args[p] = eval(t[p])

            ctx = Namespace(d=args, p=ns)

            if callable(d['f']):
                return d['f'](**args)

            return eval(d['f'], ctx, nss)


def shortform(t):
    '''
    Given a parse tree, return its canonical stringified
    short-form
    '''
    pass


def longform(t):
    '''
    Given a parse tree, return its canonical stringified
    long-form
    '''
    pass


# TODO: Arrow through REPL history. Requires intercepting 
# arrow keys from stdin.
def repl(p='\n> ', i=sys.stdin, o=sys.stdout):
    '''
    Given a stream of parse trees, evaluate each,
    and return the result.
    '''
    sys.stderr.write('(…) Tali (α) ')

    ts=parse(tokenize(i))
    while True:
        if p: print(p, end='', flush=True)
        t = next(ts)
        r = eval(t)
        print(t, flush=True)
        print(r, flush=True)


if __name__ == '__main__':
    repl(i=sys.stdin)
