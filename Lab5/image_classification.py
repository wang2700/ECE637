# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import numpy as np
import matplotlib.pyplot as plt
from training_data.read_data import read_data

# %%
X = read_data()
n = X.shape[1]
mu = np.mean(X, axis=1)
X_centered = np.zeros_like(X)
for i in range(X.shape[1]):
    X_centered[:, i] = X[:, i] - mu
Z = X/np.sqrt(X.shape[0] - 1.0)
U, S, Vt = np.linalg.svd(Z, full_matrices=False)
# R = 1/(n-1) * (np.dot(Z, Z.transpose()))


# %%
m = 10
A = U[:,:10]
Y = np.dot(A.transpose(), X_centered)


# %%
param = []
for i in range(26):
    indices = np.arange(start=i, stop=312, step=26)
    Yk = Y[:, indices]
    mu_letter = (1.0/12) * np.sum(Yk, axis=1)
    Yk_center = Yk - mu_letter.reshape(10,1)
    cov_letter = np.zeros((10,10))
    for j in range(12):
        cov = np.outer(Yk_center[:, j], Yk_center[:, j].T)
        cov_letter += cov
    cov_letter /= (1.0/11)
    param.append({'mean': mu_letter, 'cov': cov_letter})


# %%
# import test images
import os
from PIL import Image
r = 64
c = 64
X_test = np.zeros((r*c, 26))
testdir='/home/jerry/Documents/Github/ECE637/Lab5/test_data/veranda'
for c in range(ord('a'), ord('z')+1, 1):
    fname = os.path.join(testdir, chr(c) + '.tif')
    im = Image.open(fname)
    img = np.array(im)
    X_test[:, c-ord('a')] = np.reshape(img, (1,4096))


# %%
# prediction on test image
miss_pred = []
prediction = []
X_test_center = np.zeros_like(X_test)
for i in range(X_test.shape[1]):
    X_test_center = X_test[:, i] - mu
    Y_test = np.dot(A.transpose(), X_test_center)
    pred_list = np.zeros((26,1))
    for j, class_param in enumerate(param):
        cov_k = class_param['cov']
        mu_k = class_param['mean']
        # print(cov_k)
        pred_list[j] = np.dot(np.dot(Y_test-mu_k, np.linalg.inv(cov_k)),Y_test-mu_k) + np.abs(np.log(np.linalg.det(cov_k)))
    prediction.append(chr(np.argmin(pred_list) + ord('a')))
    gt = chr(i+ord('a'))
    if (prediction[i] != gt):
        miss_pred.append({'pred': prediction[i], 'gt': gt})
# print(prediction)
print(miss_pred)
# Y_test = np.dot(A.transpose(), X_test_center)
