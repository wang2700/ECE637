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


def fidelity(f, b, gamma):
    # gamma correct f
    f_correct = 255. * np.power(f / 255., gamma)
    # Low pass filter f and b
    sig_sq = 2
    kernel = np.zeros((7, 7))
    for i in range(7):
        for j in range(7):
            kernel[i, j] = math.exp(-(i ^ 2 + j ^ 2) / (2 * sig_sq))
    kernel = kernel / np.mean(kernel)
    f_filter = apply_filter(f_correct, kernel)
    b_filter = apply_filter(b, kernel)
    # apply transformation
    f_filter = np.power(255. * (f_filter / 255.), 1. / 3.)
    b_filter = np.power(255. * (b_filter / 255.), 1. / 3.)
    return np.power(np.power(np.sum(f_filter - b_filter), 2) / np.prod(f_filter.shape), 0.5)


# %% Threasholding
out_path = '/home/jerry/Documents/Github/ECE637/Lab8/'
T = 127
binary_img = np.zeros_like(img)
binary_img[img > 127] = 255
img_out = Image.fromarray(binary_img.astype(np.uint8))
img_out.save(out_path + 'part3_out.tif')
RSME = np.power(np.power(np.sum(img - binary_img), 2) /
                np.prod(img.shape), 0.5)
print('RSME: ', RSME)
fid = fidelity(img, binary_img, 2.2)
print('fidelity: ', fid)
# %% Ordered Dithering
