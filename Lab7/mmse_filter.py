# %% Import Packages
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from PIL import Image

# %% Import Image
path = '/home/jerry/Documents/Github/ECE637/Lab7/'
im = Image.open(path + 'img14bl.tif')
img_bl = np.array(im)
im = Image.open(path + 'img14g.tif')
img_g = np.array(im)
im = Image.open(path + 'img14gn.tif')
img_gn = np.array(im)
im = Image.open(path + 'img14sp.tif')
img_sp = np.array(im)
width = 768
height = 512
window_size = 7

# %% filter function


def apply_filter_at_pixel(img, i, j, theta):
    kernal_size = theta.shape[0]
    pixel = 0.0
    for k in range(theta.shape[0]):
        for l in range(theta.shape[1]):
            loc_i = i + k - kernal_size // 2
            loc_j = j + l - kernal_size // 2
            if loc_i >= 0 and loc_i < img.shape[0] and loc_j >= 0 and loc_j < img.shape[1]:
                pixel += theta[k, l] * img[loc_i, loc_j]
    return pixel


# %% Compute covariance matrix and cross correlation


def mmse_filter(img_ori, img):
    Y = img_ori[3::20, 3::20].reshape((-1,))
    N = Y.shape[0]
    Z = np.zeros((N, window_size * window_size))
    Z_ind = 0
    for i in range(3, height, 20):
        for j in range(3, width, 20):
            Z[Z_ind, :] = img[i-window_size//2:i+window_size//2 +
                              1, j-window_size//2:j+window_size//2+1].reshape((-1,))
            Z_ind += 1
    Rzz = np.dot(Z.T, Z) / N
    rzy = np.dot(Z.T, Y) / N
    # Compute Filter Coefficient theta* and apply the filter
    theta = np.dot(np.linalg.inv(Rzz), rzy).reshape((7, 7))
    img_filter = np.zeros_like(img_ori).astype(np.float)
    for i in range(height):
        for j in range(width):
            img_filter[i, j] = apply_filter_at_pixel(img_bl, i, j, theta)
    img_filter[img_filter < 0] = 0
    img_filter[img_filter > 255] = 255
    return img_filter.astype(np.uint8)


# %% show and save filtered image
gray = cm.get_cmap('gray', 256)
plt.figure
plt.imshow(mmse_filter(img_g, img_bl), cmap=gray)
plt.title('Filtered Image of img_bl.tif')
plt.savefig(path + 'filtered_bl.png')
plt.figure
plt.imshow(mmse_filter(img_g, img_gn), cmap=gray)
plt.title('Filtered Image of img_gn.tif')
plt.savefig(path + 'filtered_gn.png')
plt.figure
plt.imshow(mmse_filter(img_g, img_sp), cmap=gray)
plt.title('Filtered Image of img_bl.tif')
plt.savefig(path + 'filtered_sp.png')

# %%
