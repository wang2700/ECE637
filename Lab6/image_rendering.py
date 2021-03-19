# %%
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# %% Import Data
# Load data.npy
data = np.load('/home/jerry/Documents/Github/ECE637/Lab6/data.npy',
               allow_pickle=True)[()]
refletance = np.load(
    '/home/jerry/Documents/Github/ECE637/Lab6/reflect.npy', allow_pickle=True)[()]
R = refletance['R']
D65 = data['illum1']
florescent = data['illum2']
x0 = data['x']
y0 = data['y']
z0 = data['z']

# %% Calculate XYZ tristimulus values
option = 1
I = np.zeros_like(R)
filename = None
if option == 1:
    I = R * D65.reshape((1, 1, 31))
    filename = 'img_d65.png'
else:
    I = R * florescent.reshape((1, 1, 31))
    filename = 'img_flo.png'
XYZ = np.zeros((I.shape[0], I.shape[1], 3))
for i in range(I.shape[0]):
    for j in range(I.shape[1]):
        XYZ[i, j, 0] = sum((I[i, j, :] * x0).reshape((31,)))
        XYZ[i, j, 1] = sum((I[i, j, :] * y0).reshape((31,)))
        XYZ[i, j, 2] = sum((I[i, j, :] * z0).reshape((31,)))

# %% Transform the XYZ to RGB color space using D65
chromaticity_709 = np.array([[0.64, 0.3, 0.15],
                            [0.33, 0.6, 0.06],
                            [0.03, 0.1, 0.79]])
wp_d65 = np.array([0.3127, 0.3290, 0.3583])
weight_709_d65 = np.dot(np.linalg.inv(chromaticity_709), np.array(
    [[wp_d65[0]/wp_d65[1]], [1], [wp_d65[2]/wp_d65[1]]]))
M_709_d65 = np.dot(chromaticity_709, np.diag(weight_709_d65.reshape((3,))))
print("Transform Matrix from D65 illumination to Rec 709 RGB")
print(np.linalg.inv(M_709_d65))
RGB = np.zeros_like(XYZ)
for i in range(XYZ.shape[0]):
    for j in range(XYZ.shape[1]):
        RGB[i, j, :] = np.dot(np.linalg.inv(M_709_d65), XYZ[i, j, :])
RGB[RGB < 0] = 0
RGB[RGB > 1] = 1
gamma = 1.8
img = (RGB * 255)
img = (255 * np.power(img / 255.0, np.ones_like(img) / gamma)).astype(np.uint8)
plt.figure()
plt.imshow(img)
im_save = Image.fromarray(img)
im_save.save('/home/jerry/Documents/Github/ECE637/Lab6/' + filename, 'png')
# %%
