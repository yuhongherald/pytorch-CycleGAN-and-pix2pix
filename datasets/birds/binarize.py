import sys
import os
import cv2
import numpy as np

input = sys.argv[1]
output = sys.argv[2]

size = 3
size2 = size * 3 + 1

def apply_kernel(img, kernel): 
    return np.sum(np.multiply(img, kernel))

kernel_uniform = np.ones((size2, size2))#np.array([np.array([1, 1, 1, 1, 1]), np.array([1, 1, 1, 1, 1]), np.array([1, 1, 1, 1, 1]), np.array([1, 1, 1, 1, 1]), np.array([1, 1, 1, 1, 1])])

for file in os.listdir(input):
    #observed: Around weak edges, tend to have more low value pixels
    img = cv2.imread(os.path.join(input, file), cv2.IMREAD_GRAYSCALE)
    ret,thresh = cv2.threshold(img,127,255,cv2.THRESH_BINARY_INV)
    #apply_kernel(thresh/25, kernel_uniform)
    img2 = cv2.filter2D(thresh/size2/size2, -1, kernel_uniform)
    ret,thresh2 = cv2.threshold(img2,255 * 4 / 5,255,cv2.THRESH_BINARY)
    # 5x5 with 5 weak signals should get removed

    ret,thresh3 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)

    cv2.imwrite(os.path.join(output, file), thresh3 - thresh2)