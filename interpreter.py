import re
import sys
import signal
import argparse
from os import system
from decimal import Decimal
from inspect import isfunction

from lex import tokenize
from parse import parse, TaliSet


# TODO: I need to enforce distinction b/w values and
# symbols much more strongly. We can use atoms as keys
# in a map, but only symbols can be used as keys in
# a context
class Symbol(str): pass


class Context(dict):
    '''
    A context is a dictionary of (symbol, definition) pairs,
    with an optional parent context.

    d: dict to populate the context from

    p: parent context

    ns: namespace lookup for resolving reference
        (might not be necessary, unused for now)

    Most contexts are ephemeral, defining the short-lived
    scope of variables during the execution of a function.
    '''
    # TODO: Want to be able to declare some contexts immutable
    def __init__(self, d, p=None, ns=None):
        self.p = p
        # TODO: think about syntax and how that propagates
        self.ns = ns
        self.update(d)

    def find(self, s):
        '''
        Find the innermost context in which a given symbol
        is defined.
        '''
        if s in self: return self
        elif self.p is None: raise LookupError(s)
        else: return self.p.find(s)

    def clone(self):
        '''
        Copy is a method of dict, and returns a dict, so
        wrap that to enable cloning of a context.
        '''
        d = self.copy()
        return Context(d, self.p, self.ns)


class Procedure(object):
    '''
    An instance of a Tali procedure, consisting of
    parameters, expression, and context.
    '''
    def __init__(self, ks, e, c):
        self.ks, self.e, self.c = ks, e, c

    def __call__(self, **vs):
        pairs = {k: vs[k] for k in self.ks}
        return eval(self.e, Context(pairs, self.c))


def define(n, p, f, c):
    '''
    Given a function name, parameters, and body, as well as an
    execution context, define the respective function within the
    context.

    This is a special form; we don't evaluate f, but rather save
    it, as that is the body for the function, and it shouldn't
    (and usually can't) be evaluated until arguments are supplied
    for the function parameters.
    '''

    # TODO: Again, this list right now is indexed with
    # integers. We need to make sure that the interpeter only
    # allows symbols, and doesn't expose the implementation at
    # all
    params = []
    for i in range(p['len']):
        params.append(p[i])

    c[n] = {
        'p': params,
        'f': Procedure(params, f, c)
    }


def bind(k, v, m):
    '''
    key, value, map
    '''
    m[k] = v
    return m


def index(k, m):
    '''
    key, map
    '''
    return m[k]


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


def prnt(s):
    print(s)
    return s


# TODO: Want to return this value as a function
root = Context({
        'def': {
            'p': ['n', 'p', 'f'],
            'f': define
        },
        'bnd': {
            'p': ['k', 'v', 'm'],
            'f': bind
        },
        'idx': {
            'p': ['k', 'm'],
            'f': index
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
        },
        'print': {
            'p': ['s'],
            'f': prnt
        }
    })

# TODO: This construction should be returned via a function
# rather than sitting here, so that I can grab them and
# call eval in other contexts as well
namespaces = {'root': root}
current = 'root'

isa = isinstance

# TODO: Make tail-recursive
def eval(t, c=root, n='root', ns=namespaces):
    '''
    Tail-recursive evaluation of an parse tree in a given
    context.

    t: parse tree
    c: execution context
    n: namespace specifier
    ns: namespace collection -- is this used??

    '''
    while True:
        if isa(t, TaliSet):
            temp = {}
            for k, v in t.expressions.items():
                v = eval(v, c, n, ns)
                # TODO: this does not allow dictionaries
                # or sets to be elements of sets.

                # We have a problem here.
                # If ints and strings and symbols all evaluate
                # to the same symbol, we can't have
                # Sym(1), Int(1), and "1" all in the same set

                # That wreaks havoc on clean namespacing though.
                # Lisp handles this by? Not having this problem.

                # A stop-gap is prefixing symbols
                # to obtain a symbol form.
                # That's not a bad tradeoff.
                # sym-1
                # int-1
                # str-1
                # But that requires some significant ergonomics.
                temp[v] = v
            return temp

        # Atom
        elif not isa(t, dict):
            # TODO: if not a string, then return?
            # Just to cover other such cases
            if isa(t, int):
                return t

            # parse integers
            if re.fullmatch('[0-9]+', t):
                return int(t)

            # parse decimals
            elif re.fullmatch('[0-9]+\.[0-9]+', t):
                return Decimal(t)

            # parse strings
            elif re.fullmatch('\".*\"', t):
                return str(t[1:-1])

            elif t == '⊤':
                return True

            elif t == '⊥':
                return False

            else:
                return c.find(t)[t]

        elif '@' not in t:
            '''
            Map literal; values are reduced
            '''
            return {k:eval(v) for k, v in t.items()}

        elif t['@'] == 'def':
            define(t['n'], t['p'], t['f'], c)
            return None

        # TODO: if q is an atom, then this is really
        # returning a string. The distinction should be
        # enforced more strongly to prevent this being
        # abused.
        elif t['@'] == 'quote':
            return t['q']

        elif t['@'] == 'eval':
            return eval(eval(t['e']))

        elif t['@'] == 'if':
            '''
            Implement a conditional:

              (@: if
               p: ...
               t: ...
               f: ...)

            p for predicate
            t for true consequent
            f for false consequent

            We must only evaluate one of t or f to avoid
            a potential infinite loop that arises when
            we execute a given consequent when we shouldn't.
            '''
            pre = t['p']
            con = t['t']
            alt = t['f']
            return eval(con, c) if eval(pre, c) else eval(alt, c)

        else:
            '''
            All other function invocation ((@: ...))
            '''
            # TODO: implement partial application
            dfn = c.find(t['@'])[t['@']]
            args = {p:eval(t[p], c) for p in dfn['p']}

            if callable(f := dfn['f']):
                return f(**args)

            ctx = Context(d=args, p=c)

            return eval(dfn['f'], ctx, ns)


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


class BufferedStdin():
    '''
    Because we intercept control characters, we need
    to push those back.
    '''

    def __init__(self, stdin):
        self.stdin = stdin
        self.buffer = []

    def read(self, count):
        if len(self.buffer) != 0:
            return self.buffer.pop()
        else:
            return self.stdin.read(count)

    def store(self, c):
        self.buffer.append(c)


def repl(p='\n> ', i=sys.stdin, o=sys.stdout):
    '''
    Given a stream of parse trees, evaluate each,
    and return the result.

    :param p: prompt to print before entering S-expressions
    :param i: input file stream
    :param o: output file stream
    '''
    sys.stdout.write('(…) Tali 0.0.0 ')

    stream = BufferedStdin(i)

    ts=parse(tokenize(stream))
    while True:
        if p: print(p, end='', flush=True)

        t = next(ts)
        r = eval(t)
        print(r, flush=True)


def execute_file(name):
    # TODO: Make context reset optional
    c = root.clone()
    with open(name, 'r') as f:
        stream = BufferedStdin(f)

        ts = parse(tokenize(stream))

        for t in ts:
            print(eval(t, c))


def handler(sig, frame):
    sys.exit(0)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')

    parser.add_argument('-F', metavar='F', type=str, nargs='+',
        required=False, help='an integer for the accumulator')

    args = parser.parse_args()
    if args.F:
        for f in args.F:
            print('-' * 65)
            print(f)
            print('-' * 65)
            execute_file(f)
    else:
        signal.signal(signal.SIGINT, handler)
        repl()
