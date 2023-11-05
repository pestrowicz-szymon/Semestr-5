%{
#include <stdio.h>
FILE *outputFile;
int insideComment = 0; // Zmienna wskazująca, czy znajdujemy się wewnątrz komentarza.
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

[^<]+ {
    // Drukuje treść poza komentarzami.
    if (!insideComment) {
        fprintf(outputFile, "%s", yytext);
    }
}

"<" {
    // Początek nowego elementu.
    fprintf(outputFile, "%s", yytext);
    BEGIN INITIAL;
}

. {
    // Dowolny inny znak.
    fprintf(outputFile, "%s", yytext);
}

%%

int main(int argc, char *argv[]) {
    if (argc != 3) {
        fprintf(stderr, "Użycie: %s <plik_wejsciowy> <plik_wyjsciowy>\n", argv[0]);
        return 1;
    }

    FILE *inputFile = fopen(argv[1], "r");
    if (inputFile == NULL) {
        perror("Błąd otwarcia pliku wejściowego");
        return 1;
    }

    outputFile = fopen(argv[2], "w");
    if (outputFile == NULL) {
        perror("Błąd otwarcia pliku wyjściowego");
        return 1;
    }

    yyin = inputFile;
    yylex();

    fclose(inputFile);
    fclose(outputFile);
    return 0;
}
