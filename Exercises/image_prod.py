import numpy as np
from scipy import misc
import matplotlib.pyplot as plt
import random

img = misc.imread('labrador-600.jpg')

sepia = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)

for i in range(0, img.shape[0], 2):
    for j in range(0, img.shape[1], 2):
        r = img[i][j][0]
        g = img[i][j][1]
        b = img[i][j][2]
        sepia[i][j][0] = min(random.uniform(0.3, 0.4)*r + random.uniform(0.6, 0.8)*g + random.uniform(0.1, 0.2)*b, 255)
        sepia[i][j][1] = min(random.uniform(0.3, 0.4)*b + random.uniform(0.6, 0.8)*r + random.uniform(0.1, 0.2)*g, 255)
        sepia[i][j][2] = min(random.uniform(0.3, 0.4)*g + random.uniform(0.6, 0.8)*b + random.uniform(0.1, 0.2)*r, 255)

plt.imshow(sepia, cmap=plt.cm.gray)
plt.show()
