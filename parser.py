'''
This is a very thin, executable wrapper around syntactic
analysis.
'''
import sys
from lex import tokenize
from parse import parse

if __name__ == '__main__':
    print(list(parse(tokenize(sys.stdin))))
