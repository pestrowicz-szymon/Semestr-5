%option noyywrap
%{
#include <string>
#include "calculator.tab.h"

int yylex();
%}

%s COMMENT
%%

<INITIAL>{
#           BEGIN(COMMENT);
[ \t]+      ;
[0-9]+      { yylval = atoi(yytext); return NUM; }
\+          return PLUS; 
\-          return MINUS; 
\*          return MULTIPLY;
\/          return DIVIDE;
\^          return POW;
\(          return LBRACKET;
\)          return RBRACKET;
\n          return ENDLINE;
\\\n        ;
.           return ERROR;
}

<COMMENT>{
.|\\\n		;
\n          BEGIN(INITIAL);
}

%%