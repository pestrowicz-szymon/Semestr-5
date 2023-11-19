%{
#include <stdio.h>
int lineCount = 0;
int wordCount = 0;
%}

%x SPACE

%%

^[ \t]+ {
    // Spacje i taby na poczatku
}

[ \t]+ {
    BEGIN SPACE;
}

<SPACE>[^\n] {
    printf(" %s", yytext);
    wordCount++;
    BEGIN INITIAL;
}

<SPACE>[\n] {
    printf("\n");
    lineCount++;
    BEGIN INITIAL;
}

<SPACE><<EOF>> {
    lineCount++;
    yyterminate();
}

<<EOF>> {
    lineCount++;
    yyterminate();
}

^([ \t]*\n)+ {
    // Puste linie
}

"\n" {
    lineCount++;
    printf("\n");
}

. {
    // Dowolny inny znak
    printf("%s", yytext);
}

%%

int main(int argc, char *argv[]) {
    yylex();
    //printf("\nLiczba linii: %d\n", lineCount);
    //printf("Liczba słów: %d\n", wordCount);
    return 0;
}