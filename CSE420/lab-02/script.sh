#!/bin/bash

"$(brew --prefix bison)"/bin/bison -d -y --debug --verbose updated_syntax_analyzer.y
echo 'Generated the parser C file as well the header file'
g++ -w -c -o y.o y.tab.c
echo 'Generated the parser object file'
flex lex_analyzer.l
echo 'Generated the scanner C file'
g++ -fpermissive -w -c -o l.o lex.yy.c
echo 'Generated the scanner object file'
g++ y.o l.o -o parser
echo 'All ready, running'
./parser input.txt