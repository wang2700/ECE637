#include <math.h>
#include "tiff.h"
#include "allocate.h"
#include "randlib.h"
#include "typeutil.h"

void filter(uint8_t **img, double **output, double **kernel, int i, int j, 
                        int width, int height, int kernel_size);

void apply_color(struct TIFF_img output, double **input, int channel);

int main (int argc, char **argv)
{
  FILE *fp;
  struct TIFF_img input_img, filter_img, psf_img;
  double **output;
  double **kernel;
  int32_t i, j;
  
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

  if ((fp = fopen(argv[2], "rb")) == NULL) {
    fprintf ( stderr, "cannot open file %s\n", argv[2] );
    exit ( 1 );
  }

  if (read_TIFF(fp, &psf_img)) {
    fprintf( stderr, "error reading file %s\n", argv[2] );
    exit(1);
  }

  fclose(fp);

  //allocate memory
  output = (double **)get_img(input_img.width, input_img.height, sizeof(double));
  kernel = (double **)get_img(psf_img.width, psf_img.height, sizeof(double));

  //covert tif to kernel
  printf("Create Kernel\n");
  for (i = 0; i < psf_img.width; i++) {
    for (j = 0; j < psf_img.width; j++) {
      kernel[i][j] = psf_img.mono[i][j] / 255.0;
    }
  }

  //apply the filter
  printf("Apply filter\n");
  printf("Image size: %d %d\n", input_img.width, input_img.height);
  get_TIFF( &filter_img, input_img.height, input_img.width, 'c');
  for (int c = 0; c < 3; c++){
    for (i = 0; i < input_img.height; i++) {
      for (j = 0; j < input_img.width; j++) {
        filter(input_img.color[c], output, kernel, i, j, 
                          input_img.width, input_img.height, psf_img.width);
      }
    }
    printf("Channel %d complete\n", c);
    apply_color(filter_img, output, c);
    printf("Applied channel %d color\n", c);
  }

  /* open image file for write */
  
  if ( ( fp = fopen ( "iir_filter.tif", "wb" ) ) == NULL ) {
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
  free_TIFF(&(psf_img));
  free_img((void**)output);
  free_img((void**)kernel);
}

void filter(uint8_t **img, double **output, double **kernel, int i, int j, 
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
      output.color[channel][i][j] = (int32_t)input[i][j];
    }
  }
}
