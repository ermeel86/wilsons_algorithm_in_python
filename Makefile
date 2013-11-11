CC=clang
GCC_OPT=-O2 -Wall -Wextra 

all: lib_wilson.so lib_cluster_statistics.so 
OP=obj/
SP=src/


lib_wilson.so: wilson.o
	$(CC) $(GCC_OPT) -shared  -o $(OP)lib_wilson.so \
	   $(OP)wilson.o -lgsl -lgslcblas -lm

lib_cluster_statistics.so: cluster_statistics.o uf.o
	$(CC) $(GCC_OPT) -shared  -o $(OP)lib_cluster_statistics.so \
	   $(OP)cluster_statistics.o $(OP)uf.o -lm

wilson.o: $(SP)wilson.c $(SP)wilson.h
	$(CC) $(GCC_OPT) -fPIC -c $(SP)wilson.c -o $(OP)wilson.o

cluster_statistics.o: $(SP)cluster_statistics.c $(SP)cluster_statistics.h
	$(CC) $(GCC_OPT) -fPIC -c $(SP)cluster_statistics.c -o $(OP)cluster_statistics.o

uf.o: $(SP)uf.c $(SP)uf.h
	$(CC) $(GCC_OPT) -fPIC -c $(SP)uf.c -o $(OP)uf.o
clean:
	rm $(OP)*.o
