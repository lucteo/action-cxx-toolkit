.PHONY: all clean test

all: test_app
clean:
	rm -f $(ODIR)/*.o *~ core $(INCDIR)/*~ 

test:
	./test_app

CC=g++
CFLAGS := $(CFLAGS)
CXXFLAGS := $(CXXFLAGS)

test_app: main.cpp
	$(CC) -o test_app main.cpp $(CXXFLAGS)

