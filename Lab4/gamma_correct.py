import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from matplotlib import cm

filename = 'linear.tif'
im = Image.open('Lab4/input/' + filename)
x = np.array(im)
gamma = 1.59
y = 255 * np.power((x / 255), np.ones_like(x) * (1/gamma))

gray = cm.get_cmap('gray', 256)
plt.figure(1)
plt.imshow(x, cmap=gray)
plt.figure(2)
plt.imshow(y, cmap=gray)
plt.show()

filename = 'gamma15.tif'
im = Image.open('Lab4/input/' + filename)
x = np.array(im)
gamma_monitor = 1.59
gamma_orignal= 1.5
z = 255 * np.power((x / 255), np.ones_like(x) * (gamma_orignal/gamma_monitor))

gray = cm.get_cmap('gray', 256)
plt.figure(1)
plt.imshow(x, cmap=gray)
plt.figure(2)
plt.imshow(z, cmap=gray)
plt.figure(3)
plt.imshow(y, cmap=gray)
plt.show()