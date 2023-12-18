%{
    #include <stdio.h>
    #include <ctype.h>
    #include <stdlib.h>
    int yylex();
    struct stack_entry {
        int p;
        int v; 
    };
    void push(int prime, int value); 
    void print_stack();
    void check_if_error();
    void printer(int result);
    int add(int a, int b, int p);
    int sub(int a, int b, int p);
    int mul(int a, int b, int p);
    int divide(int a, int b, int p);
    int power(long long a, int b, int p);
    int extendedEuclideanAlgorithm(int a, int b, int *x, int *y);
    void yyerror(char const*);
    const int p1 = 1234577;
    const int p2 = 1234576;
    struct stack_entry *stack = NULL;
    int stack_size = 0;
    int flag = 0;
    int p = 0;
    int v1 = 0;
    int result = 0;
    enum {
        PLUS_VALUE = 1234578, 
        SUB_VALUE,
        NEG_VALUE,
        MUL_VALUE,
        DIV_VALUE,
        POW_VALUE,
    };

%}
%union {int num;}
%type  <num> exp
%type  <num> exp1
%token <num> NUMBER 
%token PLUS 
%token MINUS PLUS_VALUE
%token MULTIPLY 
%token DIVIDE 
%token LEFT 
%token RIGHT 
%token POWER 
%token NEWLINE 
%token COMMENT
%token UMINUS 
%left  PLUS MINUS
%left  MULTIPLY DIVIDE
%left  UMINUS
%right POWER
%start input
%%

input: 
|       input line
;

line:   NEWLINE 
|       COMMENT NEWLINE
|       error NEWLINE
|       exp NEWLINE        {check_if_error(); print_stack(); printer($1); }
;

exp:    NUMBER                  { $$ = $1%p1;              push(p1, $$);              }
|       exp PLUS exp            { $$ = add($1, $3, p1);    push(p1, PLUS_VALUE);      }
|       exp MINUS exp           { $$ = sub($1, $3, p1);    push(p1, SUB_VALUE);       }
|       exp MULTIPLY exp        { $$ = mul($1, $3, p1);    push(p1, MUL_VALUE);       }
|       exp DIVIDE exp          { $$ = divide($1, $3, p1); if($$ == -1) {flag = -1; p = p1; v1 = $3;} else {push(p1, DIV_VALUE);}}
|       MINUS exp %prec UMINUS  { $$ = p1 - $2%p1;         push(p1, NEG_VALUE);       }
|       exp POWER exp1          { $$ = power($1, $3, p1);  push(p1, POW_VALUE);       }
|       LEFT exp RIGHT          { $$ = $2;                                            }

; 
exp1:   NUMBER                  { $$ = $1%p2;              push(p2, $$);              }
|       exp1 PLUS exp1          { $$ = add($1, $3, p2);    push(p2, PLUS_VALUE);      }
|       exp1 MINUS exp1         { $$ = sub($1, $3, p2);    push(p2, SUB_VALUE);       }
|       exp1 MULTIPLY exp1      { $$ = mul($1, $3, p2);    push(p2, MUL_VALUE);       }
|       exp1 DIVIDE exp1        { $$ = divide($1, $3, p2); if($$ == -1) {flag = -1; p = p2; v1 = $3;} else {push(p2, DIV_VALUE);}}
|       MINUS exp1 %prec UMINUS { $$ = p2 - $2%p2;         push(p2, NEG_VALUE);       }
|       LEFT exp1 RIGHT         { $$ = $2;                                            }

;
%%

void print_stack() {
    for(int i = 0; i<stack_size;) {
        if (stack[i].v < p1) {
            if (i+1<stack_size && stack[i+1].v==NEG_VALUE) {
                printf("%d ", stack[i].p-stack[i].v);
                i+=2;
            }
            else {
                printf("%d ", stack[i].v);
                i++;
            }
        }
        else {
            switch(stack[i].v) {
                case PLUS_VALUE: printf("+ "); break;
                case SUB_VALUE: printf("- "); break;
                case NEG_VALUE: printf("~ "); break;
                case MUL_VALUE: printf("* "); break;
                case DIV_VALUE: printf("/ "); break;
                case POW_VALUE: printf("^ "); break;
            }
            i++;
        }
    }
    stack_size = 0;
}

void printer(int result) {
    if(flag==-1){
        flag = 0;
    }
    else {
        printf("= %d\n", result);
        flag = 0;
    }
}

void check_if_error(){
    if(flag == -1) {
        printf("> %d nie jest odwracalne modulo %d\n", v1, p);
        stack_size = 0;
    }
}

void push(int prime, int value) {
    stack = (struct stack_entry*) realloc(stack, (stack_size+1)*sizeof(struct stack_entry));
    stack[stack_size].v = value;
    stack[stack_size].p = prime;  
    stack_size++;
}

int main() {
    yyparse();
    if(stack != NULL) {
        free(stack);
    }
    return 0;
}

void yyerror(char const *s) {
   fprintf(stderr, "%s\n", s);
   stack_size = 0;
}

int add(int a, int b, int p) {
    return (a + b)%p;
}

int sub(int a, int b, int p) {
    return (a + (p - b))%p;
}

int mul(int a, int b, int p) {
    return (a * b)%p;
}

int divide(int a, int b, int p) {
    int x, y;
    long long inv;
    int g = extendedEuclideanAlgorithm(b, p, &x, &y);
    if (g != 1)
        inv = -1;
    else
        inv = (x%p + p)%p;
    a = a%p;
    if (inv == -1){
        return -1;
    }
    return (inv * a)%p;
}

int power(long long a, int b, int p) {
    int result = 1;
    if (a == 0) return 0;
    while (b > 0) {
        if (b % 2 == 1)
            result = (result * a)%p;
        b = b >> 1;
        a = (a * a)%p;
    }
    return result;
}

int extendedEuclideanAlgorithm(int a, int b, int *x, int *y) {
        if (a == 0){
            *x = 0, *y = 1;
            return b;
        }
        int x1, y1;
        int gcd = extendedEuclideanAlgorithm(b%a, a, &x1, &y1);
        *x = y1 - (b/a) *x1;
        *y = x1;
        return gcd;
}