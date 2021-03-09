# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'

import numpy as np
import matplotlib.pyplot as plt
from training_data.read_data import read_data
import os
from PIL import Image


def image_classification(X, class_params):
    miss_pred = []
    prediction = []
    X_test_center = np.zeros_like(X)
    for i in range(X.shape[1]):
        X_test_center = X[:, i] - mu
        Y_test = np.dot(A.transpose(), X_test_center)
        pred_list = np.zeros((26,1))
        for j, class_param in enumerate(class_params):
            cov_k = class_param['cov']
            mu_k = class_param['mean']
            # print(cov_k)
            pred_list[j] = np.dot(np.dot(Y_test-mu_k, np.linalg.inv(cov_k)),Y_test-mu_k) + np.log(np.abs(np.linalg.det(cov_k)))
        prediction.append(chr(np.argmin(pred_list) + ord('a')))
        gt = chr(i+ord('a'))
        if (prediction[i] != gt):
            miss_pred.append({'pred': prediction[i], 'gt': gt})
    return prediction, miss_pred

X = read_data()
n = X.shape[1]
mu = np.mean(X, axis=1)
X_center = np.zeros_like(X)
for i in range(X.shape[1]):
    X_center[:, i] = X[:, i] - mu
Z = X/np.sqrt(X.shape[0] - 1.0)
U, S, Vt = np.linalg.svd(Z, full_matrices=False)
# R = 1/(n-1) * (np.dot(Z, Z.transpose()))

m = 10
A = U[:,:10]
Y = np.dot(A.transpose(), X_center)

class_params = []
for i in range(26):
    indices = np.arange(start=i, stop=312, step=26)
    Yk = Y[:, indices]
    mu_letter = (1.0/12) * np.sum(Yk, axis=1)
    Yk_center = Yk - mu_letter.reshape(10,1)
    cov_letter = np.zeros((10,10))
    for j in range(12):
        cov = np.outer(Yk_center[:, j], Yk_center[:, j].T)
        cov_letter += cov
    cov_letter /= 11
    class_params.append({'mean': mu_letter, 'cov': cov_letter})


# import test images
r = 64
c = 64
X_test = np.zeros((r*c, 26))
testdir='/home/jerry/Documents/Github/ECE637/Lab5/test_data/veranda'
for c in range(ord('a'), ord('z')+1, 1):
    fname = os.path.join(testdir, chr(c) + '.tif')
    im = Image.open(fname)
    img = np.array(im)
    X_test[:, c-ord('a')] = np.reshape(img, (1,4096))

# First Classification attempt
prediction, miss_pred = image_classification(X_test,class_params) 
print(miss_pred)

# possibility 1
class_params = []
for i in range(26):
    indices = np.arange(start=i, stop=312, step=26)
    Yk = Y[:, indices]
    mu_letter = (1.0/12) * np.sum(Yk, axis=1)
    Yk_center = Yk - mu_letter.reshape(10,1)
    cov_letter = np.zeros((10,10))
    for j in range(12):
        cov = np.outer(Yk_center[:, j], Yk_center[:, j].T)
        cov_letter += cov
    cov_letter /= 11
    cov_letter = np.diag(np.diagonal(cov_letter))
    class_params.append({'mean': mu_letter, 'cov': cov_letter})
prediction, miss_pred = image_classification(X_test, class_params)
print('Miss Prediction for 1')
print(miss_pred)



# Probability 2
Rwc = np.zeros((10,10))
class_params = []
for i in range(26):
    indices = np.arange(start=i, stop=312, step=26)
    Yk = Y[:, indices]
    mu_letter = (1.0/12) * np.sum(Yk, axis=1)
    Yk_center = Yk - mu_letter.reshape(10,1)
    cov_letter = np.zeros((10,10))
    for j in range(12):
        cov = np.outer(Yk_center[:, j], Yk_center[:, j].T)
        cov_letter += cov
    cov_letter /= 11
    class_params.append({'mean': mu_letter, 'cov': Rwc})
    Rwc += cov_letter
Rwc /= 26.0
for i in range(26):
    class_params[i]['cov'] = Rwc
prediction, miss_pred = image_classification(X_test, class_params)
print('Miss Prediction for 2')
print(miss_pred)

# Probability 3
cov_letter = np.diag(np.diagonal(Rwc))
for i in range(26):
    class_params[i]['cov'] = cov_letter
prediction, miss_pred = image_classification(X_test, class_params)
print('Miss Prediction for 3')
print(miss_pred)

# Probability 4
cov_letter = np.diag(np.diagonal(np.ones((10,10))))
for i in range(26):
    class_params[i]['cov'] = cov_letter
prediction, miss_pred = image_classification(X_test, class_params)
print('Miss Prediction for 4')
print(miss_pred)