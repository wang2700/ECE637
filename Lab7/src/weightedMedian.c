#include <math.h>
#include "tiff.h"
#include "allocate.h"
#include "randlib.h"
#include "typeutil.h"

uint8_t weightedMeanFilter(uint8_t **img,
                           double **weight,
                           int i, int j,
                           int width, int height,
                           int weight_size);
void swap(int *a, int *b);
void selectionSort(int arr1[], int arr2[], int n);
int sum(int arr1[], int start, int end);

int main(int argc, char const *argv[])
{
  FILE *fp;
  struct TIFF_img input_img, filter_img;
  double **output;
  int weight_size = 5;
  double **weight;

  // check for argument count
  if (argc != 2)
  {
    fprintf(stderr, "Missing Argument\n");
    exit(1);
  }

  //check for error in reading files
  if ((fp = fopen(argv[1], "rb")) == NULL)
  {
    fprintf(stderr, "cannot open file %s\n", argv[1]);
    exit(1);
  }

  // check for reading tiff file
  if (read_TIFF(fp, &input_img))
  {
    fprintf(stderr, "error reading file %s\n", argv[1]);
    exit(1);
  }

  fclose(fp);

  if (input_img.TIFF_type != 'g')
  {
    fprintf(stderr, "error:  image must be greyscale\n");
    exit(1);
  }

  //allocate memory for the output image
  output = (double **)get_img(input_img.width, input_img.height,
                              sizeof(double));
  weight = (double **)get_img(weight_size, weight_size,
                              sizeof(double));

  //generate weight
  for (int i = 0; i < weight_size; i++)
  {
    for (int j = 0; j < weight_size; j++)
    {
      if (i == 1 || i == weight_size - 1 ||
          j == 1 || j == weight_size - 1)
      {
        weight[i][j] = 1.0;
      }
      else
      {
        weight[i][j] = 2.0;
      }
    }
  }

  //apply the filter
  get_TIFF(&filter_img, input_img.height, input_img.width, 'g');
  for (int i = 0; i < input_img.height; i++)
  {
    for (int j = 0; j < input_img.width; j++)
    {
      filter_img.mono[i][j] = weightedMeanFilter(input_img.mono,
                                                 (double **)weight,
                                                 i, j,
                                                 input_img.width,
                                                 input_img.height,
                                                 weight_size);
    }
  }

  if ((fp = fopen("output.tif", "wb")) == NULL)
  {
    fprintf(stderr, "cannot open file output.tif\n");
    exit(1);
  }

  if (write_TIFF(fp, &filter_img))
  {
    fprintf(stderr, "cannot write to file output.tif\n");
    exit(1);
  }

  fclose(fp);

  free_img((void **)output);
  free_TIFF(&(input_img));
  free_TIFF(&(filter_img));
  return 0;
}

uint8_t weightedMeanFilter(uint8_t **img,
                           double **weight,
                           int i, int j,
                           int width, int height,
                           int weight_size)
{
  int pixels[weight_size * weight_size];
  int weights[weight_size * weight_size];
  int maxPixels = 0;

  //extact pixels and weights
  for (int k = 0; k < weight_size; k++)
  {
    for (int l = 0; l < weight_size; l++)
    {
      int loc_i = i + k - weight_size / 2;
      int loc_j = j + l - weight_size / 2;
      if (loc_i >= 0 && loc_i < height &&
          loc_j >= 0 && loc_j < width)
      {

        pixels[k * weight_size + l] = img[loc_i][loc_j];
        weights[k * weight_size + l] = weight[k][l];
        maxPixels++;
      }
    }
  }

  // sort the pixels
  selectionSort(pixels, weights, maxPixels);

  // find the median
  int median_idx;
  for (int i = 0; i < maxPixels; i++)
  {
    if (sum(weights, 0, i) >= sum(weights, i + 1, maxPixels))
    {
      median_idx = i;
      break;
    }
  }
  return pixels[median_idx];
}

void swap(int *a, int *b)
{
  int temp = *a;
  *a = *b;
  *b = temp;
}

void selectionSort(int arr1[], int arr2[], int n)
{
  int i, max_idx;

  for (i = 0; i < n - 1; i++)
  {
    max_idx = i;
    for (int j = i + 1; j < n; j++)
    {
      if (arr1[j] > arr1[max_idx])
        max_idx = j;

      swap(&arr1[max_idx], &arr1[i]);
      swap(&arr2[max_idx], &arr2[i]);
    }
  }
}

int sum(int arr[], int start, int end)
{
  int sum = 0;
  for (int i = start; i <= end; i++)
  {
    sum += arr[i];
  }
  return sum;
}