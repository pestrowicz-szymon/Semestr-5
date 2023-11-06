%{
#include <stdio.h>
int insideComment = 0;
%}

%x COMMENT

%%
"<!--" {
    BEGIN COMMENT;
    insideComment = 1;
}

<COMMENT>.|\n {
    // Pomijamy treść komentarza.
}

<COMMENT>"-->" {
    BEGIN INITIAL;
    insideComment = 0;
}

. {
    // Dowolny inny znak.
    printf("%s", yytext);
}

%%

int main(int argc, char *argv[]) {
    yylex();
    return 0;
}
