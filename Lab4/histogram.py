import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from matplotlib import cm

def equalize(x):
    # calculate histogram of x
    h,_ = np.histogram(x)
    
    # calculate cumulative distribution of x
    F = np.zeros((256,))
    for i in range(256):
        F[i] = np.sum(h[0:i]) / np.sum(h)
    
    # equalize the image
    y = np.zeros_like(x)
    for i in range(x.shape[0]):
        for j in range(x.shape[1]):
            y[i,j] = F[x[i,j]]
    z = np.zeros_like(x)

filename = 'kids.tif'
im = Image.open('input/' + filename)
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

equalize(x)


