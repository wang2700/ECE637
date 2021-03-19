# %%
import numpy as np
import matplotlib.pyplot as plt

# %% Import Data
# Load data.npy
data = np.load('/home/jerry/Documents/Github/ECE637/Lab6/data.npy', allow_pickle=True)[()]
# List keys of dataset
data.keys()

# %% 
wv = np.arange(400, 701, 10)
chromaticity = np.zeros((3, wv.shape[0]+1))
for i in range(wv.shape[0]):
    XYZ = np.array([[data['x'][:,i]],[data['y'][:,i]],[data['z'][:,i]]]).reshape((3,))
    chromaticity[:,i] =  XYZ / np.sum(XYZ)
chromaticity[:,wv.shape[0]] = chromaticity[:,0]
plt.figure(figsize=(8,8))
plt.plot(chromaticity[0,:], chromaticity[1,:], label='Pure Spectral Source')

# CIE_1931
chromaticity_CIE = np.array([[0.73467, 0.27376, 0.16658, 0.73467],
                            [0.26533, 0.71741, 0.00886, 0.26533],
                            [0.0, 0.00883, 0.82456, 0.0]])
plt.plot(chromaticity_CIE[0,:], chromaticity_CIE[1,:], 'r-', label=r'$CIE_{1931}$')
plt.text(chromaticity_CIE[0,0], chromaticity_CIE[1,0], r'$CIE_{1931}$ - Red', fontsize='large', color='red')
plt.text(chromaticity_CIE[0,1], chromaticity_CIE[1,1], r'$CIE_{1931}$ - Green', fontsize='large', color='red')
plt.text(chromaticity_CIE[0,2], chromaticity_CIE[1,2], r'$CIE_{1931}$ - Blue', fontsize='large', color='red')

# Rec 709
chromaticity_709 = np.array([[0.64, 0.3, 0.15, 0.64],
                            [0.33, 0.6, 0.06, 0.33],
                            [0.03, 0.1, 0.79, 0.03]])
plt.plot(chromaticity_709[0,:], chromaticity_709[1,:], 'g-', label=r'Rec. 709')
plt.text(chromaticity_709[0,0], chromaticity_709[1,0], r'Rec. 709 - Red', fontsize='large', color='green')
plt.text(chromaticity_709[0,1], chromaticity_709[1,1], r'Rec. 709 - Green', fontsize='large', color='green')
plt.text(chromaticity_709[0,2], chromaticity_709[1,2], r'Rec. 709 - Blue', fontsize='large', color='green')

# D65
plt.plot(0.3127, 0.329, 'mo', label='D65 White Point')
plt.text(0.3127, 0.3, 'D65 White Point', color='magenta', fontsize='large')

# Equal Energy
plt.plot(0.333, 0.333, 'ko', label='Equal Energy White Point')
plt.text(0.333, 0.34, 'Equal Energy White Point', color='black', fontsize='large')

plt.legend()