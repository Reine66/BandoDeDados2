#!/usr/bin/python

import sys

#entrada de stdin
for line in  sys.stdin:
    #remove espaços em branco
    line = line.strip()
    #quebra linha em palavras
    words = line.split()

    for word in words:
        print('%s\t%s' % (word.lower(), 1))