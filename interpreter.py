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
            tokens = tokens[1:]
        else:
            if tokens[0][0] != 'LPAREN':
                print("Error: expected '('")
                sys.exit(0)

            print(tokens[0])
            tokens = tokens[1:]
            match_kv_list()

            if tokens[0][0] != 'RPAREN':
                print("Error: expected ')'")
                sys.exit(0)

            print(tokens[0])
            tokens = tokens[1:]

    def match_kv_list():
        nonlocal tokens
        print('matching kv list')
        match_kv_pair()

        if tokens[0][0] == 'COMMA':
            print(tokens[0])
            tokens = tokens[1:]
            match_kv_list()

    def match_kv_pair():
        print('matching kv pair')
        nonlocal tokens

        match_atom()

        if tokens[0][0] != 'COLON':
            print("Error: expected ':'")
            sys.exit(0)

        print(tokens[0])
        tokens = tokens[1:]

        match_expr()
                
    def match_atom():
        print('matching atom')
        nonlocal tokens

        if (tokens[0][0] == 'ATOM'):
            print(tokens[0])
            tokens = tokens[1:]

    match_expr()


test1 = '' \
    '(f: add-two,' \
    ' a: (a: 1,' \
         'b: 2))'

print(tokenize(test1))
print('\n\n')
parse(tokenize(test1))
