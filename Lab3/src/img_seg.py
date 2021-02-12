import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib as mpl

# Read in a segmentation TIFF image.
for filename in {"T1", "T2", "T3"}:
    im = Image.open('/home/jerry/Documents/Github/ECE637/Lab3/demo/section2/'+ filename + '.tif')

    x = np.array(im)

    N = np.max(x)

    cmap = mpl.colors.ListedColormap(np.random.rand(N+1,3))
    plt.imshow(x, cmap=cmap)
    plt.colorbar()
    plt.title('Image')
    plt.show()