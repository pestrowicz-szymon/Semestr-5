%{
#include <stdio.h>
int savedoxygen = 0;
%}

%x SINGLE_LINE MULTIPLE_LINE MULTIPLE_LINE_DOXYGEN

%%
"//" { BEGIN(SINGLE_LINE); }
<SINGLE_LINE>[^\n]*(\n?) { printf("%s", "\n"); BEGIN(INITIAL); }
"///"[^\n]*(\n?) {if (savedoxygen==1) printf("%s", yytext); else printf("%s", "\n"); } 
"//!"[^\n]*(\n?) {if (savedoxygen==1) printf("%s", yytext); else printf("%s", "\n"); } 

"/*" { BEGIN(MULTIPLE_LINE); }
<MULTIPLE_LINE>"*/" { BEGIN(INITIAL); }
<MULTIPLE_LINE>. { /* Zostań w stanie MULTIPLE_LINE */ }

"/**" {if (savedoxygen==1) printf("%s", yytext); BEGIN(MULTIPLE_LINE_DOXYGEN); } 
"/*!" {if (savedoxygen==1) printf("%s", yytext); BEGIN(MULTIPLE_LINE_DOXYGEN); }
<MULTIPLE_LINE_DOXYGEN>"*/" { if (savedoxygen==1) printf("%s", yytext); BEGIN(INITIAL); }
<MULTIPLE_LINE_DOXYGEN>. { if (savedoxygen==1) printf("%s", yytext); /* Zostań w stanie MULTIPLE_LINE */ }


"\n" {
    printf("%s", "\n");
}

. {
    // Dowolny inny znak.
    printf("%s", yytext);
}
%%

int main(int argc, char *argv[]) {
    savedoxygen = atoi(argv[1]);
    yylex();
    return 0;
}
