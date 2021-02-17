import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from matplotlib import cm

def equalize(x):
    # calculate histogram of x
    h,_ = np.histogram(x, bins=np.linspace(0,255,256))
    
    # calculate cumulative distribution of x
    F = np.zeros((256,))
    for i in range(256):
        F[i] = np.sum(h[0:i]) / np.sum(h)
    
    # equalize the image
    y = np.ones_like(x, dtype=float)
    for i in range(x.shape[0]):
        for j in range(x.shape[1]):
            x_temp = x[i,j]
            f_temp = F[x_temp]
            y[i,j] = F[x_temp]
    y_min = y.min()
    y_max = y.max()
    z = 255 * (y - y_min) / (y_max - y_min)
    z = z.astype(dtype=int)
    return z, F

filename = 'kids.tif'
im = Image.open('Lab4/input/' + filename)
x = np.array(im)
gray = cm.get_cmap('gray', 256)
plt.figure(1)
plt.imshow(x, cmap=gray)
plt.figure(2)
plt.hist(x.flatten(), bins=np.linspace(0,255,256))
plt.title('Histogram of ' + filename)
plt.xlabel('Pixel Value')
plt.ylabel('Number of Pixels')
plt.show()

z, F = equalize(x)
plt.figure(3)
plt.plot(np.linspace(0, 255, 256), F)
plt.title('Cumulative Distribution of kids.tif')
plt.xlabel('Pixel Value')
plt.ylabel('Cumulative Probability')

plt.figure(4)
plt.hist(z.flatten(), bins=np.linspace(0,255,256))
plt.title('Histogram of Equalized Image of kids.tif')
plt.xlabel('Pixel Value')
plt.ylabel('Number of Pixels')

plt.figure(5)
plt.imshow(z, cmap=gray)
plt.show()
