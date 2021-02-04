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
    ax.set_title('Power Spectral Density of y')

    fig.colorbar(surf, shrink=0.5, aspect=5)

    plt.show()

def iir_filter(x, y, i, j):
    sum = 3 * x[i][j]
    if i - 1 >= 0:
        sum += 0.99 * y[i-1][j]
    if j - 1 >= 0:
        sum += 0.99 * y[i][j-1]
    if i - 1 >= 0 and j - 1 >= 0:
        sum -= 0.9801 * y[i-1][j-1]
    y[i][j] = sum
    
            

x = np.random.uniform(low=-0.5, high=0.5, size=(512,512))
x_scaled = 255 * (x + 0.5)
y = np.zeros_like(x)

for i in range(512):
    for k in range(512):
        iir_filter(x, y, i, k)

y_scaled = y.astype(int) + 127

# Display numpy array by matplotlib.
plt.imshow(x_scaled, cmap=plt.cm.gray)
plt.title('Image x')
plt.show()

plt.imshow(y_scaled, cmap=plt.cm.gray)
plt.title('Image y')
plt.show()

a = b = np.linspace(start=-np.pi, stop=np.pi, num=64)
Sy = np.zeros((64,64), dtype=np.float)
X, Y = np.meshgrid(a, b)

i = 0
for u in a:
    Sy[i] = np.abs(3/(1-0.99*np.exp(-1j*u)-0.99*np.exp(-1j*b)+0.9801*np.exp(-1j*u-1j*b)))**2 * (1.0/12)
    i += 1

Sy_log = np.log(Sy)

fig = plt.figure(figsize=(10,8))
ax = fig.add_subplot(111, projection='3d')
surf = ax.plot_surface(X, Y, Sy_log, cmap=plt.cm.coolwarm)

ax.set_xlabel('$\mu$ axis')
ax.set_ylabel('$\\nu$ axis')
ax.set_zlabel('Z Label')
ax.set_title('Theoretical Power Spectral Density')

fig.colorbar(surf, shrink=0.5, aspect=5)

BetterSpecAnal(y)