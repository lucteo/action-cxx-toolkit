.PHONY: all clean

all: test_app
clean:
	rm -f $(ODIR)/*.o *~ core $(INCDIR)/*~ 

CC=gcc

test_app: main.c
	$(CC) -o test_app main.c

