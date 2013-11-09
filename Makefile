CC=clang
GCC_OPT=-O2 -Wall -Wextra 

all: lib_wilson.so 
OP=obj/
SP=src/
#PPFIX=\"/home/elcie/Simulations/RCM_Fragmentation/\"
PPFIX=\"/home/eren/Research/Simulations/Wilsons_Algorithm_UST/\"


lib_wilson.so: wilson.o
	$(CC) $(GCC_OPT) -shared  -o $(OP)lib_wilson.so \
	   $(OP)wilson.o -lgsl -lgslcblas -lm

wilson.o: $(SP)wilson.c $(SP)wilson.h
	$(CC) $(GCC_OPT) -fPIC -c $(SP)wilson.c -o $(OP)wilson.o
clean:
	rm $(OP)*.o
