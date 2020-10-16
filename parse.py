'''
Grammar:
Expr = Atom |
       ( KVList )

KVList = KVPair , KVList | Empty

KVPair = Atom: Expr
'''
import sys

namespaces = {}

def parse(tokens):

    def match_expr():
        nonlocal tokens
        print('matching expression')

        t = tokens[0]

        if t.name() == 'ATOM':
            print(t)
            tokens = tokens[1:]
            return ('EXPR', t.value())
        else:
            children = []
            if t.name() != 'LPAREN':
                print('Error: expected "("')
                sys.exit(0)

            print(t)
            children.append(t)
            tokens = tokens[1:]
            children.append(match_kv_list())

            t = tokens[0]

            if t.name() != 'RPAREN':
                print('Error: expected ")"')
                sys.exit(0)

            print(t)
            children.append(t)
            tokens = tokens[1:]
            return ('EXPR', children)

    def match_kv_list():
        nonlocal tokens
        print('matching kv list')
        children = []
        children.append(match_kv_pair())

        t = tokens[0]

        if t.name() == 'COMMA':
            print(t)
            children.append(t)
            tokens = tokens[1:]
            children.append(match_kv_list())

        print('kv list matched')
        return ('KVL', children)

    def match_kv_pair():
        print('matching kv pair')
        nonlocal tokens

        children = []

        children.append(match_atom())

        t = tokens[0]

        if t.name() != 'COLON':
            print("Error: expected ':'")
            sys.exit(0)

        print(t)
        children.append(t)

        tokens = tokens[1:]

        children.append(match_expr())

        # Otherwise, epsilon production
        print('kv pair matched')
        return ('KVP', children)

    def match_atom():
        print('matching atom')
        nonlocal tokens

        t = tokens[0]

        if (t.name() == 'ATOM'):
            print(t)
            val = t
            tokens = tokens[1:]
            return t.value()

    return match_expr()
