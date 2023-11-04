%{
#include <stdio.h>
#include <stdbool.h>
#include <math.h>

int pointer = 0;
int stos[20];
bool blad = false;
void push(int i);
int pop();

int yylex();
%}

%%

"-"?[0-9]+	push(atoi(yytext));

"+" 	if(blad==false){
		int temp2 = pop(); 
		int temp1 = pop(); 
		push(temp1 + temp2);
	}
					 
			
"-" 	if(blad==false){
		int temp2 = pop(); 
		int temp1 = pop(); 
		push(temp1 - temp2);
	}
				 
			
"*" 	if(blad==false){
		int temp2 = pop(); 
		int temp1 = pop(); 
		push(temp1 * temp2);
	}
			
"/" 	if(blad==false){
		int temp2 = pop(); 
		int temp1 = pop(); 
		if(temp2!=0){
			push(temp1 / temp2);
		}else{
			printf("Dzielenie przez 0\n");
			blad=true;
		}
	}
					 
			
"%" 	if(blad==false){
		int temp2 = pop(); 
		int temp1 = pop(); 
		if(temp2!=0){
			push(temp1 % temp2);
		}else{
			printf("Dzielenie przez 0\n");
			blad=true;
		}
	}
					 
			
"^" 	if(blad==false){
		int temp2 = pop(); 
		int temp1 = pop(); 
		push((int)pow(temp1, temp2));
	}				 
			


\n	{	if((pointer!=1)&&(blad==false)){
			printf("Za mala liczba operatorow\n");
		}else if(blad==false){
			printf("=%d\n",stos[1]);				
		}
		
		blad = false;
		pointer = 0;
	}

[ \t]+		;
[^ \t]		printf("Zly symbol \n"); blad = true;
			
%%

int pop() {
	if (pointer>0){
		pointer--;
		return stos[pointer+1];
	}
	else{
		blad = true;
		printf("Za mala liczba argumentow\n");	
		return 0;
	}
}

void push(int i) {
	pointer++;
	stos[pointer]= i;
}

int main() { 
   yylex(); 
}