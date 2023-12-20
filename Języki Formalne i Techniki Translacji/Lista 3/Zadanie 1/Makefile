FLAGS = -W -O3

.PHONY = all clean cleanall

all: calc

calc: parser.y scanner.l
	bison -o parser_y.c -d parser.y
	flex -o scanner_l.c scanner.l
	$(CC) $(FLAGS) -o calc parser_y.c scanner_l.c

clean:
	rm -f *.c *.h

cleanall: clean
	rm -f calc