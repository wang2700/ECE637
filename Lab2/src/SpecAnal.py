#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 24 18:54:16 2021

@author: Wenrui Li
"""

import numpy as np                 # Numpy is a library support computation of large, multi-dimensional arrays and matrices.
from PIL import Image              # Python Imaging Library (abbreviated as PIL) is a free and open-source additional library for the Python programming language that adds support for opening, manipulating, and saving many different image file formats.
import matplotlib.pyplot as plt    # Matplotlib is a plotting library for the Python programming language.

def BetterSpecAnal(x):
    W = np.hamming(64).reshape((64,1))*np.hamming(64).reshape((1,64))
    i_c = x.shape[0] / 2
    j_c = x.shape[1] / 2 
    loc_i = np.zeros((25,))
    loc_j = np.zeros((25,))
    # Calculate Location of all windows
    for i in range(-2,3):
        for j in range(-2,3):
            loc_i[(i+2)*5+(j+2)] = i_c + i * 64
            loc_j[(i+2)*5+(j+2)] = j_c + j * 64
    
    loc_i = loc_i.astype(int)
    loc_j = loc_j.astype(int)
    Z = np.zeros((64,64))
    for ind in range(25):
        i = loc_i[ind]
        j = loc_j[ind]
        z = x[i-32:i+32, j-32:j+32]
        Z_temp = (1/64**2) * np.abs(np.fft.fft2(z))**2
        Z = Z + np.log(np.fft.fftshift(Z_temp))
    Z = Z / 25
    # Plot the result using a 3-D mesh plot 
    fig = plt.figure(figsize=(10,8))
    ax = fig.add_subplot(111, projection='3d')
    a = b = np.linspace(-np.pi, np.pi, num = 64)
    X, Y = np.meshgrid(a, b)

    surf = ax.plot_surface(X, Y, Z, cmap=plt.cm.coolwarm)

    ax.set_xlabel('$\mu$ axis')
    ax.set_ylabel('$\\nu$ axis')
    ax.set_zlabel('Z Label')

    fig.colorbar(surf, shrink=0.5, aspect=5)

    plt.show()



# Read in a gray scale TIFF image.
im = Image.open('/home/jerry/Documents/Github/ECE637/Lab2/input/img04g.tif')
print('Read img04.tif.')
print('Image size: ', im.size)

# Display image object by PIL.
# im.show(title='image')

# Import Image Data into Numpy array.
# The matrix x contains a 2-D array of 8-bit gray scale values. 
x = np.array(im)
print('Data type: ', x.dtype)

# Display numpy array by matplotlib.
plt.imshow(x, cmap=plt.cm.gray)
plt.title('Image')

# Set colorbar location. [left, bottom, width, height].
cax =plt.axes([0.9, 0.15, 0.04, 0.7]) 
plt.colorbar(cax=cax)
plt.show()

x = np.double(x)/255.0

i = 99
j = 99
N =64
print('Block Size: ', N)

z = x[i:N+i, j:N+j]

# Compute the power spectrum for the NxN region.
Z = (1/N**2)*np.abs(np.fft.fft2(z))**2

# Use fftshift to move the zero frequencies to the center of the plot.
Z = np.fft.fftshift(Z)

# Compute the logarithm of the Power Spectrum.
Zabs = np.log(Z)

# Plot the result using a 3-D mesh plot and label the x and y axises properly. 
fig = plt.figure(figsize=(10,8))
ax = fig.add_subplot(111, projection='3d')
a = b = np.linspace(-np.pi, np.pi, num = N)
X, Y = np.meshgrid(a, b)

surf = ax.plot_surface(X, Y, Zabs, cmap=plt.cm.coolwarm)

ax.set_xlabel('$\mu$ axis')
ax.set_ylabel('$\\nu$ axis')
ax.set_zlabel('Z Label')

fig.colorbar(surf, shrink=0.5, aspect=5)

plt.show()

BetterSpecAnal(x)