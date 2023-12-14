%{
#include <stdio.h>
#include "operations.cpp"

bool minusAreEven = true;

int yylex(void);
void yyerror(const char *) {};
%}

%define api.value.type {int}
%token NUM
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
|   exp DIVIDE exp          { $$ = divide($1, $3); if(errorOccured) {errorOccured = false; YYERROR;}}
|   exp POW exp             { $$ = power($1, $3); }
|   MINUS NUM               { addNumber(-$2); $$ = -$2; }
|   LBRACKET exp RBRACKET   { $$ = $2; }
|   MINUS LBRACKET exp RBRACKET   { $$ = -$3; addMinus(); }
;

%%

int main() {
    return yyparse();
}