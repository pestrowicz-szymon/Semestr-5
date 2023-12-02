%{
#include <stdio.h>
#include "operations.cpp"

int yylex(void);
void yyerror(const char *) {};
%}

%define api.value.type {int}
%token NUM
%precedence NEG
%left PLUS
%left MINUS
%left MULTIPLY
%left DIVIDE
%right POW
%token LBRACKET
%token RBRACKET
%token ENDLINE
%token ERROR

%%

input:
    %empty
|   input line
;

line:
    ENDLINE
|   exp ENDLINE         { showResult($1); }
|   error ENDLINE       { handleError(); }
;

exp:
    NUM                     { addNumber($1); }
|   exp PLUS exp            { $$ = add($1, $3); }
|   exp MINUS exp           { $$ = sub($1, $3); }
|   exp MULTIPLY exp        { $$ = mul($1, $3); }
|   exp DIVIDE exp          { $$ = divide($1, $3); }
|   exp POW NUM             { addExpNumber($3); $$ = power($1, $3); }
|   exp POW MINUS NUM       { addExpNumber(-$3); $$ = power($1, -$3); }
|   MINUS NUM %prec NEG     { addNumber(-$2); $$ = -$2; }
|   LBRACKET exp RBRACKET   { $$ = $2; }
;

%%

int main() {
    return yyparse();
}