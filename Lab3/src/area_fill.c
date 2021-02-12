#include "tiff.h"
#include "allocate.h"
#include "randlib.h"
#include "typeutil.h"
#include "segmentation.h"

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

  seg = (unsigned int **)get_img(input_img.width, 
                                  input_img.height, 
                                  sizeof(unsigned int));

  ConnectedSet(s, T, input_img.mono, input_img.width, 
                input_img.height, label, seg, &NumOfPixel);

  printf("Found %d pixels\n", NumOfPixel);

  get_TIFF(&seg_img, input_img.height, input_img.width, 'g');
  for (int i = 0; i < seg_img.height; i++) {
    for (int j = 0; j < seg_img.width; j++) {
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