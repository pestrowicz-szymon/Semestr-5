%{
#include <stdio.h>
int insideComment = 0;
int inquote = 0;
int bracket = 0;
%}

%x COMMENT

%%
"<!--" {
    if (inquote == 0) {
        BEGIN COMMENT;
        insideComment = 1;
    } else {
        printf("<!--");
    }
}

<COMMENT>.|\n {
    // Pomijamy treść komentarza.
}

<COMMENT>"-->" {
    BEGIN INITIAL;
    insideComment = 0;
}

"<" { bracket = 1; printf("<"); }
">" { bracket = 0; printf(">"); }

"\"" { 
    if (bracket==1) {
        if (inquote==0) 
            inquote = 1; 
        else 
            inquote = 0; 
    }
    printf("\"");
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
