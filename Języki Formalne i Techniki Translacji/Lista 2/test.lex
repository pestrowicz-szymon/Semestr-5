%{
#include <stdio.h>
int yywrap();
int yylex();

    char* concat(const char* str1, const char* str2) {
        char* result = malloc(strlen(str1) + strlen(str2) + 1);
        strcpy(result, str1);
        strcat(result, str2);
        return result;
    }

    int err = 0;
    char* str = "";

    int docs = 1;
%}

singleline      \/[\\\n]*\/
singlelineDoc   \/[\\\n]*\/(\/|!)
multiline       \/[\\\n]*\*
multilineDoc    \/[\\\n]*\*[\\\n]*(\*|!)
multilineEnd    \*[\\\n]*\/

%x singleLine
%x multiLine
%x string
%x include

%%
{singlelineDoc}             { if (docs) ECHO; else BEGIN(singleLine); };
{singleline}                BEGIN(singleLine);
<singleLine>.*\\\n          ;
<singleLine>.               ;
<singleLine>[^\\]\n         BEGIN(INITIAL);


{multilineDoc}              { if (docs) ECHO; else BEGIN(multiLine); };
{multiline}                 BEGIN(multiLine);
<multiLine>.|\n             ;
<multiLine>{multilineEnd}   BEGIN(INITIAL);

\"                          { ECHO; BEGIN(string); };
<string>\"                  { ECHO; BEGIN(INITIAL); };

#include[[:blank:]]*\<      { ECHO; BEGIN(include); };
<include>\>                 { ECHO; BEGIN(INITIAL); };
<include>.|\n               ECHO;
               
%%
int yywrap() {
    return 1;
}
int main() {
    return yylex();
}