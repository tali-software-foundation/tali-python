import lex as l
import parse as p

# TODO: This is where we have a symbol table

test1 = '' \
    '(f: +,' \
    ' a: (a: 1,' \
         'b: 2))'

def visit(tree):
    return visit_expr(tree)


def visit_expr(expr):
    None


def visit_atom(atom):
    return atom[1]


print(l.tokenize(test1))
print('\n\n')

tree = p.parse(l.tokenize(test1))
print('\n\n')

print(tree)

print(visit(tree))
