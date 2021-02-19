import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from matplotlib import cm

def stretch(input, T1, T2):
    slope = 255.0 / (T2 - T1)
    output = np.zeros_like(input)
    for i in range(input.shape[0]):
        for j in range(input.shape[1]):
            if (input[i,j] > T1 and input[i,j] <= T2):
                output[i,j] = int((input[i,j] - T1) * slope)
            elif (input[i,j] > T2):
                output[i,j] = 255
    return output

filename = 'kids.tif'
im = Image.open('Lab4/input/' + filename)
x = np.array(im)
T1 = 80
T2 = 160
img_stretch = stretch(x, T1, T2)
gray = cm.get_cmap('gray', 256)
plt.figure(1)
plt.imshow(img_stretch, cmap=gray)
plt.figure(2)
plt.hist(img_stretch.flatten(), bins=np.linspace(0,255,256))
plt.title('Histogram of ' + filename)
plt.xlabel('Pixel Value')
plt.ylabel('Number of Pixels')
plt.figure(3)
plt.imshow(x, cmap=gray)
plt.show()
