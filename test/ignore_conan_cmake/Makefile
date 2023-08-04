.PHONY: all clean

all: test_app
clean:
	rm -f $(ODIR)/*.o *~ core $(INCDIR)/*~ 

CXX=clang

test_app: main.cpp
	$(CXX) -o test_app main.cpp -lstdc++

