#include "tiff.h"
#include "allocate.h"
#include "randlib.h"
#include "typeutil.h"
#include "segmentation.h"

void RemoveClassLabel(struct pixel s, int width, int height, 
                      int ClassLabel, unsigned int **seg);

int main(int argc, char **argv)
{
  FILE *fp;
  struct TIFF_img input_img, seg_img;
  unsigned int **seg;
  struct pixel s;
  double T;
  int NumofRegion = 1;
  int NumofPixel = 1;

  if ( argc != 3) {
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

  T = atof(argv[2]);

  seg = (unsigned int **)get_img(input_img.width, input_img.height, 
                                  sizeof(unsigned int));

  for (int i = 0; i < input_img.height; i++) {
      for (int j = 0; j < input_img.width; j++) {
          if (seg[i][j] == 0) {
            
            s.m = i;
            s.n = j;
            ConnectedSet(s, T, input_img.mono, input_img.width, 
                          input_img.height, NumofRegion++, seg, 
                          &NumofPixel);       
            if (NumofPixel <= 100) {
              RemoveClassLabel(s, input_img.width, input_img.height, 
                              --NumofRegion, seg);
            }
            NumofPixel = 1;
          }
      }
  }

  printf("Found %d regions\n", NumofRegion);

  get_TIFF(&seg_img, input_img.height, input_img.width, 'g');
  for (int i = 0; i < seg_img.height; i++) {
    for (int j = 0; j < seg_img.width; j++) {
      // printf("%d, %d\n", i,j);
      seg_img.mono[i][j] = seg[i][j];
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

void RemoveClassLabel(struct pixel s, int width, int height, 
                        int ClassLabel, unsigned int **seg)
{
  // int M = 0;
  seg[s.m][s.n] = 0;
  struct pixel s_next;
  if (s.n - 1 >= 0) {
    if (seg[s.m][s.n-1] == ClassLabel) {
      seg[s.m][s.n-1] = 0;
      s_next.m = s.m;
      s_next.n = s.n - 1;
      RemoveClassLabel(s_next, width, height, ClassLabel, seg);
    }
  }

  if (s.m - 1 >= 0) {
    if (seg[s.m-1][s.n] == ClassLabel) {
      seg[s.m-1][s.n] = 0;
      s_next.m = s.m - 1;
      s_next.n = s.n;
      RemoveClassLabel(s_next, width, height, ClassLabel, seg);
    }
  }
  if (s.n + 1 < width) {
    if (seg[s.m][s.n+1] == ClassLabel) {
      seg[s.m][s.n+1] = 0;
      s_next.m = s.m;
      s_next.n = s.n + 1;
      RemoveClassLabel(s_next, width, height, ClassLabel, seg);
    }
  }

  if (s.m + 1 < height) {
    if (seg[s.m+1][s.n] == ClassLabel) {
      seg[s.m+1][s.n] = 0;
      s_next.m = s.m + 1;
      s_next.n = s.n;
      RemoveClassLabel(s_next, width, height, ClassLabel, seg);
    }
  }
  
}