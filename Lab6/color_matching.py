# %%
import numpy as np
import matplotlib.pyplot as plt

# %% Import Data
# Load data.npy
data = np.load('/home/jerry/Documents/Github/ECE637/Lab6/data.npy', allow_pickle=True)[()]
# List keys of dataset
data.keys()

# %% Plot x0, y0, z0
wv = np.arange(400, 701, 10)
plt.figure(figsize=(8,8))
plt.plot(wv, data['x'].reshape((31,)), '-r', label=r'$x_0(\lambda)$')
plt.plot(wv, data['y'].reshape((31,)), '-g', label=r'$y_0(\lambda)$')
plt.plot(wv, data['z'].reshape((31,)), '-b', label=r'$z_0(\lambda)$')
plt.legend()
plt.xlabel('Wavelength (nm)')
plt.ylabel('Intensity')
plt.title(r'Plot of $x_0, y_0, z_0$')
plt.show()


# %% Plot of l_0, m_0, s_0
inv_A = np.array([[0.243, 0.856, -0.044],
                  [-0.391, 1.165, 0.087],
                  [0.01, -0.008, 0.563]])
LMN = np.zeros((3, data['x'].shape[1]))
for i in range(data['x'].shape[1]):
    XYZ = np.array([[data['x'][:,i]],[data['y'][:,i]],[data['z'][:,i]]]).reshape((3,1))
    LMN[:,i] = np.dot(inv_A, XYZ).reshape((3,))

plt.figure(figsize=(8,8))
plt.plot(wv, LMN[0,:].reshape((31,)), '-r', label=r'$l_0(\lambda)$')
plt.plot(wv, LMN[1,:].reshape((31,)), '-g', label=r'$m_0(\lambda)$')
plt.plot(wv, LMN[2,:].reshape((31,)), '-b', label=r'$n_0(\lambda)$')
plt.legend()
plt.xlabel('Wavelength (nm)')
plt.ylabel('Intensity')
plt.title(r'Plot of $l_0, m_0, n_0$')
plt.show()
# %% plot D_65 and fluorescent illuminants
plt.figure(figsize=(8,8))
plt.plot(wv, data['illum1'].reshape((31,)), '-g', label=r'$D_65$')
plt.plot(wv, data['illum2'].reshape((31,)), '-b', label=r'fluorescent')
plt.legend()
plt.xlabel('Wavelength (nm)')
plt.ylabel('Intensity')
plt.title(r'Plot of $D_65$ and Fluorescent illuminants')
plt.show()
# %%
