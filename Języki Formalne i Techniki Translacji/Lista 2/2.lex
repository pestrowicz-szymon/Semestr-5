%{
#include <stdio.h>
int insideComment = 0;
int inquote = 0;
int bracket = 0;
int indata = 0;
%}

%x COMMENT

%%
"<!--" {
    if (inquote == 0 && indata == 0) {
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

"<" {
    if (inquote==0) {
        bracket = 1; 
    } 
    printf("<"); 
}
">" { 
    if (inquote==0) {
        bracket = 0; 
    }
    printf(">"); 
}

"<![CDATA" {
    printf("<![CDATA");
    indata = 1;
}
"]]>" {
    printf("]]>");
    indata = 0;
}

"\"" { 
    if (bracket==1) {
        if (inquote==0) {
            //printf("CUDZY");
            inquote = 1; 
        }
        else {
            //printf("KONIEC");
            inquote = 0; 
        }
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
