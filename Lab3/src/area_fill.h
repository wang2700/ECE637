#include <math.h>
#include "tiff.h"
#include "allocate.h"
#include "randlib.h"
#include "typeutil.h"

struct pixel
{
  int m,n;    /* m=row, n=col */
};

void ConnectedNeighbors(
  struct pixel s,
  double T,
  unsigned char **img,
  int width,
  int height,
  int *M,
  struct pixel c[4]
);

void ConnectedSet(
  struct pixel s,
  double T,
  unsigned char **img,
  int width,
  int height,
  int ClassLabel,
  unsigned int **seg,
  int *NumConPixels
);