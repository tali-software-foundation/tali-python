import sys
import string

def tokenize(program):
    # Remove all whitespace
    program = ''.join(program.split())

    tokens = []
    s = ''
    
    while len(program) > 0:
        s = program[0] 
        program = program[1:]

        reserved = ['(', ')', ':', ',']

        if s == '(':
            tokens.append(('LPAREN', '('))

        elif s == ')':
            tokens.append(('RPAREN', ')'))

        elif s == ':':
            tokens.append(('COLON', ':'))

        elif s == ',':
            tokens.append(('COMMA', ','))

        else:
            n = program[0]
            while n not in reserved:
                s = s + n
                program = program[1:]
                n = program[0]

            tokens.append(('ATOM', s))

    return tokens

def parse(tokens):

    def match_expr():
        nonlocal tokens
        print('matching expression')

        if tokens[0][0] == 'ATOM':
            print(tokens[0])
            value = tokens[0]
            tokens = tokens[1:]
            return value
        else:
            children = []
            if tokens[0][0] != 'LPAREN':
                print("Error: expected '('")
                sys.exit(0)

            print(tokens[0])
            children.append(tokens[0])
            tokens = tokens[1:]
            children.append(match_kv_list())

            if tokens[0][0] != 'RPAREN':
                print("Error: expected ')'")
                sys.exit(0)

            print(tokens[0])
            children.append(tokens[0])
            tokens = tokens[1:]
            return children

    def match_kv_list():
        nonlocal tokens
        print('matching kv list')
        children = []
        children.append(match_kv_pair())

        if tokens[0][0] == 'COMMA':
            print(tokens[0])
            children.append(tokens[0])
            tokens = tokens[1:]
            children.append(match_kv_list())

        return children

    def match_kv_pair():
        print('matching kv pair')
        nonlocal tokens

        children = []

        children.append(match_atom())

        if tokens[0][0] != 'COLON':
            print("Error: expected ':'")
            sys.exit(0)

        print(tokens[0])
        children.append(tokens[0])

        tokens = tokens[1:]

        children.append(match_expr())

        # Otherwise, epsilon production
        return children
                
    def match_atom():
        print('matching atom')
        nonlocal tokens

        if (tokens[0][0] == 'ATOM'):
            print(tokens[0])
            val = tokens[0]
            tokens = tokens[1:]
            return val 

    return match_expr()


test1 = '' \
    '(f: add-two,' \
    ' a: (a: 1,' \
         'b: 2))'

print(tokenize(test1))
print('\n\n')

tree = parse(tokenize(test1))
print('\n\n')

print(tree)
