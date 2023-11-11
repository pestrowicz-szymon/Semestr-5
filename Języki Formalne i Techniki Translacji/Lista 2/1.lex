%{
#include <stdio.h>
int lineCount = 0;
int wordCount = 0;
int inWhiteSpace = 0;
%}

%%
[ \t]+ {
    if (inWhiteSpace == 0) {
        printf(" ");
        inWhiteSpace = 1;
    }
}

[^\n \t]+ {
    if (inWhiteSpace == 1) {
        inWhiteSpace = 0;
    }
    printf("%s", yytext);
    wordCount++;
}

\n {
    if (inWhiteSpace == 1) {
        inWhiteSpace = 0;
    }
    lineCount++;
    printf("\n");
}

^([ \t]*\n)+ {
    // Puste linie
}

^[ \t]*[^ \t\n] {
    //spacje i taby na poczatku
}

[ \t]+(\n|$) {
    printf("\n");
    lineCount++
    //spacje i taby na koncu
}

. {
    // Dowolny inny znak
    printf("%s", yytext);
}

%%

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Użycie: %s <nazwa_pliku_wejściowego>\n", argv[0]);
        return 1;
    }

    FILE *file = fopen(argv[1], "r");
    if (file == NULL) {
        perror("Błąd otwierania pliku");
        return 1;
    }

    yyin = file;
    yylex();

    printf("\nLiczba linii: %d\n", lineCount);
    printf("Liczba słów: %d\n", wordCount);

    fclose(file);
    return 0;
}