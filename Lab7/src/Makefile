# For Linux or any machines with gcc compiler
CC = gcc 
CFLAGS = -std=c99 -Wall -pedantic
BIN = ../bin

all: weightedMedian

clean:
	/bin/rm *.o $(BIN)/*

OBJ = tiff.o allocate.o randlib.o qGGMRF.o solve.o

weightedMedian: weightedMedian.o $(OBJ) 
	$(CC) $(CFLAGS) -o weightedMedian weightedMedian.o $(OBJ) -lm
	mv weightedMedian $(BIN)