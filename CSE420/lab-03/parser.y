%{
#include <stdio.h>
#include <fstream>
#include "symbol_info.h"
#define YYSTYPE symbol_info*

extern FILE *yyin;
int lines = 1;
ofstream outlog;
%}

%token IF ELSE FOR WHILE DO BREAK CONTINUE RETURN INT FLOAT CHAR VOID DOUBLE
%token SWITCH CASE DEFAULT PRINTLN ADDOP MULOP INCOP DECOP RELOP
%token ASSIGNOP LOGICOP NOT LPAREN RPAREN LCURL RCURL LTHIRD RTHIRD
%token SEMICOLON COMMA ID CONST_INT CONST_FLOAT

%%

program: /* empty */
       ;

%%

int main(int argc, char *argv[]) {
    if(argc != 2) {
        printf("Please provide input file name and try again\n");
        return 1;
    }
    
    FILE *fin = fopen(argv[1], "r");
    if(fin == NULL) {
        printf("Cannot open input file\n");
        return 1;
    }
    
    yyin = fin;
    yyparse();
    fclose(fin);
    
    return 0;
}

void yyerror(char *s) {
    printf("Error at line %d: %s\n", lines, s);
} 