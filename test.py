import io

import lex as l
import parse as p
import interpret as i

test1 = '' \
    '(f: +,' \
    ' a: (a: 1,' \
         'b: 2))'

print(list([x for x in l.tokenize(io.StringIO(test1))]))
#print('\n\n')
#
#tree = p.parse(l.tokenize(test1))
#print('\n\n')
#
#print(tree)
