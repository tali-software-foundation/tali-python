'''
This is a very thin, executable wrapper around lexical
analysis.
'''
import sys
import lex

if __name__ == '__main__':
    print(*list(lex.tokenize(sys.stdin)), sep='\n')
