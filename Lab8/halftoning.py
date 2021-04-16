# %%
from PIL import Image
import numpy as np
import math

# %% Load image
im = Image.open('/home/jerry/Documents/Github/ECE637/Lab8/house.tif')
img = np.array(im).astype(np.float)


# %% filter function


def apply_filter_at_pixel(img, i, j, kernel):
    kernal_size = kernel.shape[0]
    pixel = 0.0
    for k in range(kernel.shape[0]):
        for l in range(kernel.shape[1]):
            loc_i = i + k - kernal_size // 2
            loc_j = j + l - kernal_size // 2
            if loc_i >= 0 and loc_i < img.shape[0] and loc_j >= 0 and loc_j < img.shape[1]:
                pixel += kernel[k, l] * img[loc_i, loc_j]
    return pixel

# %% FIR Filter


def apply_filter(img, kernel):
    img_filter = np.zeros_like(img)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            img_filter[i, j] = apply_filter_at_pixel(img, i, j, kernel)
    return img_filter

# %% Fidelity Function


def fidelity(f, b):
    # Low pass filter f and b
    kernel = np.zeros((7, 7)).astype(np.float)
    for i in range(7):
        for j in range(7):
            kernel[i, j] = math.exp(-((i-3) ** 2 + (j-3) ** 2) / 4.)
    kernel = kernel / np.sum(kernel)
    f_filter = apply_filter(f, kernel)
    b_filter = apply_filter(b, kernel)
    # apply transformation
    f_filter = 255. * (f_filter / 255.) ** (1. / 3.)
    b_filter = 255. * (b_filter / 255.) ** (1. / 3.)
    return np.sqrt(np.sum(np.power(f_filter - b_filter, 2)) / np.prod(f_filter.shape))


# %% Threasholding
print('Simple Thresholding')
out_path = '/home/jerry/Documents/Github/ECE637/Lab8/'
T = 127
binary_img = np.zeros_like(img)
binary_img[img > 127] = 255
img_out = Image.fromarray(binary_img.astype(np.uint8))
img_out.save(out_path + 'part3_out.tif')
RSME = np.sqrt(np.sum(np.power(img - binary_img, 2)) / np.prod(img.shape))
print('RSME: ', RSME)
img_correct = 255. * np.power(img / 255., 2.2)
fid = fidelity(img_correct, binary_img)
print('fidelity: ', fid)

# %% Bayer threashold matrix


def bayer_dither_matrix(n):
    if (n != 2):
        In = bayer_dither_matrix(n / 2)
        return np.block([[4 * In + 1, 4 * In + 2],
                         [4 * In + 3, 4 * In]])
    else:
        return np.array([[1., 2.], [3., 0.]])


def bayer_threashold(n):
    I = bayer_dither_matrix(n)
    return 255. * (I + 0.5) / (n ** 2)

# %% Apply Ordered Dithering Threashold


def apply_ordered_dithering(img, thresh):
    b = np.zeros_like(img)
    N = thresh.shape[0]
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img[i, j] > thresh[i % N, j % N]:
                b[i, j] = 255
    return b


# %% Ordered Dithering
print('Ordered Dithering')
out_path = '/home/jerry/Documents/Github/ECE637/Lab8/'
img_correct = 255. * np.power(img / 255., 2.2)
n_vec = [2, 4, 8]
for n in n_vec:
    print("Matrix Size: ", n)
    T = bayer_threashold(n)
    print(T)
    b = apply_ordered_dithering(img_correct, T)
    img_out = Image.fromarray(b.astype(np.uint8))
    img_out.save(out_path + 'part4_' + str(n) + '_out.tif')
    RSME = np.sqrt(np.sum(np.power(img - b, 2)
                          ) / np.prod(img_correct.shape))
    print('RSME: ', RSME)
    fid = fidelity(img_correct, b)
    print('fidelity: ', fid)

# %% Error Diffusion
out_path = '/home/jerry/Documents/Github/ECE637/Lab8/'
T = 127
img_correct = 255. * np.power(img / 255., 2.2)
output_img = np.zeros_like(img_correct)
for i in range(output_img.shape[0]):
    for j in range(output_img.shape[1]):
        if (img_correct[i, j] > T):
            output_img[i, j] = 255.
        else:
            output_img[i, j] = 0.

        error = img_correct[i, j] - output_img[i][j]
        if (j + 1 < img.shape[1]):
            img_correct[i][j+1] += 7. / 16. * error

        if (i + 1 < img.shape[0] and j + 1 < img.shape[1]):
            img_correct[i+1][j+1] += error / 16.

        if (i + 1 < img.shape[0]):
            img_correct[i+1][j] += 5. / 16. * error

        if (i + 1 < img.shape[0] and j - 1 >= 0):
            img_correct[i+1][j-1] += 3. / 16. * error
RSME = np.sqrt(np.sum(np.power(img - output_img, 2)
                      ) / np.prod(img.shape))
print('Error Diffusion')
print('RSME: ', RSME)
img_correct = 255. * np.power(img / 255., 2.2)
fid = fidelity(img_correct, output_img)
print('fidelity: ', fid)
img_out = Image.fromarray(output_img.astype(np.uint8))
img_out.save(out_path + 'part5_out.tif')
# %%
