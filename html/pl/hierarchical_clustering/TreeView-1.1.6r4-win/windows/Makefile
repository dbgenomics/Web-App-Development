

setup.exe: setup.o resources.o
	gcc -ansi -pedantic -mwindows -mno-cygwin -O4 setup.o resources.o \
	  -lole32 -luuid -o setup.exe

setup.o: setup.c resources.h
	gcc -ansi -pedantic -mno-cygwin -mwindows -Wall -fno-strict-aliasing \
	  -c -O4 setup.c

resources.o: resources.rc resources.h
	windres -i resources.rc -o resources.o

clean:
	rm -f *.o
	rm -f *.exe
