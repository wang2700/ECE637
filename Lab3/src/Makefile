# For Linux or any machines with gcc compiler
CC = gcc 
CFLAGS = -std=c99 -Wall -pedantic
BIN = ../bin

all: area_fill img_seg

clean:
	/bin/rm *.o $(BIN)/*

OBJ = tiff.o allocate.o randlib.o segmentation.o

area_fill: area_fill.o $(OBJ) 
	$(CC) $(CFLAGS) -o area_fill area_fill.o $(OBJ) -lm
	mv area_fill $(BIN)

img_seg: img_seg.o $(OBJ) 
	$(CC) $(CFLAGS) -o img_seg img_seg.o $(OBJ) -lm
	mv img_seg $(BIN)