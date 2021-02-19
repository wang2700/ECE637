import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import sys

# grey_level = int(sys.argv[1])
# grey_level = 127s
for grey_level in range(155, 166):
    img = np.zeros((256,256))
    checker = np.array([[255, 255, 0, 0],
                        [255, 255, 0, 0],
                        [0, 0, 255, 255],
                        [0, 0, 255, 255]])
    grey_board = np.ones((4,4)) * grey_level
    for i in range(int(256/8)):
        for j in range(int(256/4)):
            if (i % 4 <= 1):
                img[i*8:i*8+4,j*4:j*4+4] = checker
                img[i*8+4:i*8+8,j*4:j*4+4] = checker
            else:
                img[i*8:i*8+4,j*4:j*4+4] = grey_board
                img[i*8+4:i*8+8,j*4:j*4+4] = grey_board

    gray = cm.get_cmap('gray', 256)
    plt.figure(1)
    plt.imshow(img, cmap=gray)
    plt.title(str(grey_level))
    plt.show()