#include <math.h>
#include <stdio.h>
#include "segmentation.h"

void ConnectedNeighbors(struct pixel s, double T, unsigned char **img,
  int width, int height, int *M, struct pixel c[4])
{
  *M = 0;
  if (s.n - 1 >= 0) {
    if (abs(img[s.m][s.n] - img[s.m][s.n-1]) <= T) {
      c[*M].m = s.m;
      c[*M].n = s.n - 1;
      *M = *M + 1;
    }
  }

  if (s.m - 1 >= 0) {
    if (abs(img[s.m][s.n] - img[s.m-1][s.n]) <= T) {
      c[*M].m = s.m - 1;
      c[*M].n = s.n;
      *M = *M + 1;
    }
  }
  if (s.n + 1 < width) {
    if (abs(img[s.m][s.n] - img[s.m][s.n+1]) <= T) {
      c[*M].m = s.m;
      c[*M].n = s.n + 1;
      *M = *M + 1;
    }
  }

  if (s.m + 1 < height) {
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
  int M = 0;
  seg[s.m][s.n] = ClassLabel;
  struct pixel c[4];
  ConnectedNeighbors(s, T, img, width, height, &M, c);
  if (M == 0) {
    return;
  }
  else {
    for (int i = 0; i < M; i++) {
      struct pixel s_check = c[i];
      if (seg[s_check.m][s_check.n] != ClassLabel) {
        seg[s_check.m][s_check.n] = ClassLabel;
        *NumConPixels = *NumConPixels + 1;
        ConnectedSet(s_check, T, img, width, height, ClassLabel, seg, NumConPixels);
      }
    }
  }
}