# %%
import numpy as np
import matplotlib.pyplot as plt

# %% generate value of x, y, z
x, y = np.meshgrid(np.arange(0,1.001,0.005), np.arange(0,1.001,0.005))
z = 1 - x - y
M_709 = np.array([[0.64, 0.3, 0.15],
                [0.33, 0.6, 0.06],
                [0.03, 0.1, 0.79]])
rgb = np.zeros((z.shape[0], z.shape[1], 3))
for i in range(z.shape[0]):
    for j in range(z.shape[1]):
        rgb[i, j, :] = np.dot(np.linalg.inv(M_709), np.array([x[i,j], y[i,j], z[i,j]]).T)
rgb[rgb[:,:,0] < 0, :] = 1
rgb[rgb[:,:,1] < 0, :] = 1
rgb[rgb[:,:,2] < 0, :] = 1
gamma = 2.2
img = (255 * np.power(rgb, np.ones_like(rgb) / gamma)).astype(np.uint8)
plt.figure(figsize=(6,6))
plt.imshow(img, extent=[0,1,0,1], origin='lower')

# plot chormaticity plot of a pure spectral source
data = np.load('/home/jerry/Documents/Github/ECE637/Lab6/data.npy', allow_pickle=True)[()]
wv = np.arange(400, 701, 10)
chromaticity = np.zeros((3, wv.shape[0]+1))
for i in range(wv.shape[0]):
    XYZ = np.array([[data['x'][:,i]],[data['y'][:,i]],[data['z'][:,i]]]).reshape((3,))
    chromaticity[:,i] =  XYZ / np.sum(XYZ)
chromaticity[:,wv.shape[0]] = chromaticity[:,0]
plt.plot(chromaticity[0,:], chromaticity[1,:], label='Pure Spectral Source')
plt.title('Chormaticity diagram of Rec. 709 RGB color')
plt.savefig('/home/jerry/Documents/Github/ECE637/Lab6/709chormaticity.png')

