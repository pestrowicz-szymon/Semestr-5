%option noyywrap
%{
    #include <stdlib.h>
    #include "parser_y.h"
    void yyerror(const char *s);
%}
%%
[ \t]+              {} 
#.*                 {return COMMENT;}
\\\n                {}
\n		            {return NEWLINE;}
"+"		            {return PLUS;}
"-"		            {return MINUS;}
"*"		            {return MULTIPLY;}
"/"		            {return DIVIDE;}
"("		            {return LEFT;}
")"		            {return RIGHT;}
"^"                 {return POWER;}
[0-9]+              {yylval.num = atoi(yytext); return NUMBER;}
%%