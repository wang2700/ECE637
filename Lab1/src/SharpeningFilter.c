#include <math.h>
#include "tiff.h"
#include "allocate.h"
#include "randlib.h"
#include "typeutil.h"

void fir_filter(uint8_t **img, double **output, double **kernel, int i, int j, 
                        int width, int height, int kernel_size);

void apply_color(struct TIFF_img output, double **input, int channel);

int main (int argc, char **argv)
{
  FILE *fp;
  struct TIFF_img input_img, filter_img;
  double **output;
  int kernel_size = 5;
  double **kernel;
  int32_t i, j;
  double lambda;
  
  // check for argument count
  if ( argc != 3 ) {
    fprintf( stderr, "Missing Argument\n");
    exit(1);
  }

  //check for error in reading files
  if ( ( fp = fopen ( argv[1], "rb" ) ) == NULL ) {
    fprintf ( stderr, "cannot open file %s\n", argv[1] );
    exit ( 1 );
  }

  // check for reading tiff file
  if (read_TIFF(fp, &input_img)) {
    fprintf( stderr, "error reading file %s\n", argv[1] );
    exit(1);
  }

  fclose(fp);

  if (input_img.TIFF_type != 'c') {
    fprintf ( stderr, "error:  image must be 24-bit color\n" );
    exit ( 1 );
  }

  sscanf(argv[2], "%lf", &lambda);

  //allocate memory
  output = (double **)get_img(input_img.width, input_img.height, sizeof(double));
  kernel = (double **)get_img(kernel_size, kernel_size, sizeof(double));

  //create kernel
  printf("Create Kernel\n");
  for (i = 0; i < kernel_size; i++) {
    for (j = 0; j < kernel_size; j++) {
      if (i == kernel_size / 2 && j == kernel_size / 2) {
        kernel[i][j] = 1.0 + lambda * (1.0 - 1.0/25.0);
      } else {
        kernel[i][j] = lambda * (-1.0/25.0);
      }
    }
  }

  for (i = 0; i < kernel_size; i++) {
    for (j = 0; j < kernel_size; j++) {
      printf("%f,", kernel[i][j]);
    }
    printf("\n");
  }
  //apply the filter
  printf("Apply filter\n");
  printf("Image size: %d %d\n", input_img.width, input_img.height);
  get_TIFF( &filter_img, input_img.height, input_img.width, 'c');
  for (int c = 0; c < 3; c++){
    for (i = 0; i < input_img.height; i++) {
      for (j = 0; j < input_img.width; j++) {
        fir_filter(input_img.color[c], output, kernel, i, j, 
                          input_img.width, input_img.height, kernel_size);
      }
    }
    printf("Channel %d complete\n", c);
    apply_color(filter_img, output, c);
    printf("Applied channel %d color\n", c);
  }

  /* open image file for write */
  
  if ( ( fp = fopen ( "sharpen.tif", "wb" ) ) == NULL ) {
    fprintf ( stderr, "cannot open file lowpass_filter.tif\n");
    exit ( 1 );
  }

  /* write green image */
  if ( write_TIFF ( fp, &filter_img ) ) {
    fprintf ( stderr, "error writing TIFF file %s\n", argv[2] );
    exit ( 1 );
  }

  /* close green image file */
  fclose ( fp );

  /* de-allocate memory */
  free_TIFF(&(input_img));
  free_TIFF(&(filter_img));
  free_img((void**)output);
  free_img((void**)kernel);
}

void fir_filter(uint8_t **img, double **output, double **kernel, int i, int j, 
                        int width, int height, int kernel_size) 
{
  double sum = 0.0;
  for (int k = 0; k < kernel_size; k++) {
    for (int l = 0; l < kernel_size; l++) {
      int loc_i = i + k - kernel_size / 2;
      int loc_j = j + l - kernel_size / 2;
      if (loc_i >= 0 && loc_i < height && loc_j >= 0 && loc_j < width) {
        sum += kernel[k][l] * img[loc_i][loc_j];
      }
    }
  }
  output[i][j] = sum;
}

void apply_color(struct TIFF_img output, double **input, int channel)
{
  for (int i = 0; i < output.height; i++) {
    for (int j = 0; j < output.width; j++) {
      int32_t pixel = (int32_t)input[i][j];
      if (pixel > 255) {
        pixel = 255;
      }
      if (pixel < 0) {
        pixel = 0;
      }
      output.color[channel][i][j] = (int32_t)input[i][j];
    }
  }
}
