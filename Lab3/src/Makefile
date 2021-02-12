# For Linux or any machines with gcc compiler
CC = gcc 
CFLAGS = -std=c99 -Wall -pedantic
BIN = ../bin

all: area_fill

clean:
	/bin/rm *.o $(BIN)/*

OBJ = tiff.o allocate.o randlib.o

area_fill: area_fill.o $(OBJ) 
	$(CC) $(CFLAGS) -o area_fill area_fill.o $(OBJ) -lm
	mv area_fill $(BIN)