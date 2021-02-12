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

int main(int argc, char **argv)
{
  FILE *fp;
  struct TIFF_img input_img, seg_img;
  unsigned int **seg;
  struct pixel s;
  double T;
  int label;
  int NumOfPixel = 1;

  if ( argc != 6 ) {
    fprintf( stderr, "Missing Argument\n");
    exit(1);
  }

  if ((fp = fopen(argv[1], "rb")) == NULL) {
    fprintf(stderr, "cannot open file %s\n", argv[1]);
    exit(1);
  }

  if (read_TIFF(fp, &input_img)) {
    fprintf(stderr, "error reading file %s\n", argv[1]);
    exit(1);
  }

  fclose(fp);
  
  s.m = atoi(argv[2]);
  s.n = atoi(argv[3]);
  T = atof(argv[4]);
  label = atoi(argv[5]);

  seg = (unsigned int **)get_img(input_img.width, input_img.height, sizeof(unsigned int));

  ConnectedSet(s, T, input_img.mono, input_img.width, input_img.height, label, seg, &NumOfPixel);

  printf("Found %d pixels\n", NumOfPixel);

  get_TIFF(&seg_img, input_img.height, input_img.width, 'g');
  for (int i = 0; i < seg_img.height; i++) {
    for (int j = 0; j < seg_img.width; j++) {
      // printf("%d, %d\n", i,j);
      if (seg[i][j]) {
        seg_img.mono[i][j] = 255;
      }
    }
  }

  if ((fp = fopen("output.tif", "wb"))== NULL) {
    fprintf(stderr, "cannot open file output.tif\n");
    exit(1);
  }

  if (write_TIFF(fp, &seg_img)) {
    fprintf(stderr, "cannot write to file output.tif\n");
    exit(1);
  }

  fclose(fp);

  free_img((void**)seg);
  free_TIFF(&(input_img));
  free_TIFF(&(seg_img));
}

void ConnectedNeighbors(struct pixel s, double T, unsigned char **img,
  int width, int height, int *M, struct pixel c[4])
{
  *M = 0;
  if (s.n - 1 >= 0) {
    // printf("Check top\n");
    // printf("%d, %d\n", img[s.m][s.n], img[s.m][s.n-1]);
    if (abs(img[s.m][s.n] - img[s.m][s.n-1]) <= T) {
      c[*M].m = s.m;
      c[*M].n = s.n - 1;
      *M = *M + 1;
    }
  }

  if (s.m - 1 >= 0) {
    // printf("Check left\n");
    // printf("%d, %d\n", img[s.m][s.n], img[s.m-1][s.n]);
    if (abs(img[s.m][s.n] - img[s.m-1][s.n]) <= T) {
      c[*M].m = s.m - 1;
      c[*M].n = s.n;
      *M = *M + 1;
    }
  }
  if (s.n + 1 < width) {
    // printf("Check bottom\n");
    // printf("%d, %d\n", img[s.m][s.n], img[s.m][s.n+1]);
    if (abs(img[s.m][s.n] - img[s.m][s.n+1]) <= T) {
      c[*M].m = s.m;
      c[*M].n = s.n + 1;
      *M = *M + 1;
    }
  }

  if (s.m + 1 < height) {
    // printf("Check right\n");
    // printf("%d, %d\n", width, height);
    // printf("%d, %d\n", img[s.m][s.n], img[s.m+1][s.n]);
    if (abs(img[s.m][s.n] - img[s.m+1][s.n]) <= T) {
      c[*M].m = s.m + 1;
      c[*M].n = s.n;
      *M = *M + 1;
    }
  }
}

void ConnectedSet(struct pixel s, double T, unsigned char **img, int width,
  int height, int ClassLabel, unsigned int **seg, int *NumConPixels)
{
  // printf("Check at location %d, %d\n", s.m, s.n);
  int M = 0;
  seg[s.m][s.n] = ClassLabel;
  struct pixel c[4];
  ConnectedNeighbors(s, T, img, width, height, &M, c);
  // printf("M: %d\n", M);
  if (M == 0) {
    return;
  }
  else {
    for (int i = 0; i < M; i++) {
      struct pixel s_check = c[i];
      if (seg[s_check.m][s_check.n] != ClassLabel) {
        seg[s_check.m][s_check.n] = ClassLabel;
        *NumConPixels = *NumConPixels + 1;
        // printf("Num of Pixel: %d\n", *NumConPixels);
        ConnectedSet(s_check, T, img, width, height, ClassLabel, seg, NumConPixels);
      }
    }
  }
}