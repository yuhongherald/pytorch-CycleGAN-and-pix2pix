import sys
import os
import cv2
import numpy as np
import tqdm

input = sys.argv[1]
output = sys.argv[2]
size = 2#int(sys.argv[3]) #3
grey_threshold = 127#int(sys.argv[4]) #127
percent = 0#float(sys.argv[5]) #4 / 5

size2 = size * 4 + 1
size3 = size * 2 + 1

kernel_uniform = np.ones((9, 9), np.uint8)
kernel2 = np.ones((5, 5), np.uint8)#np.array([np.array([1, 1, 1, 1, 1]), np.array([1, 1, 1, 1, 1]), np.array([1, 1, 1, 1, 1]), np.array([1, 1, 1, 1, 1]), np.array([1, 1, 1, 1, 1])])
kernel = np.ones((3, 3), np.uint8)

coords = [[0, -1], [0, 1], [-1, 0], [1, 0]]
coords_diag = [[-1, -1], [-1, 1], [1, -1], [1, 1]]
coords_ext = coords + coords_diag

def isWhite_small(x, y, raw_image):
    if x < 0 or y < 0 or x >= raw_image.shape[0] or y >= raw_image.shape[1]:
        return False
    return raw_image[x][y] > 0

def isWhite(x, y, index, coord_arr, raw_image):
    x += coord_arr[index][0]
    y += coord_arr[index][1]
    if x < 0 or y < 0 or x >= raw_image.shape[0] or y >= raw_image.shape[1]:
        return False
    return raw_image[x][y] > 0

def getNumNeighbors(x, y, index, coord_arr, raw_image):
    x += coord_arr[index][0]
    y += coord_arr[index][1]
    result = 0
    for i in range(8):
        # remember to negative
        result += isWhite(x, y, i, coords_ext, raw_image)
    return result
    #return (isWhite(x-1,y,raw_image) +
    #    isWhite(x+1,y,raw_image) +
    #    isWhite(x,y-1,raw_image) +
    #    isWhite(x,y+1,raw_image))

def isErodable(x, y, raw_image):
    for i in range(8):
        if isWhite(x, y, i, coords_ext, raw_image) and getNumNeighbors(x, y, i, coords_ext, raw_image) <= 3:
                return False
    return True

for folder in os.listdir(input):
    if not os.path.isdir(os.path.join(input, folder)):
        continue
    path = os.path.join(input, folder)
    outpath = os.path.join(output, folder)
    if not os.path.exists(outpath):
        os.mkdir(outpath)
    for file in tqdm.tqdm(os.listdir(path), ascii=True, desc=folder , unit='|image|'):

        #observed: Around weak edges, tend to have more low value pixels
        img = cv2.imread(os.path.join(input, folder, file), cv2.IMREAD_GRAYSCALE)
        #ret,thresh = cv2.threshold(img,grey_threshold,255,cv2.THRESH_BINARY_INV)
        #img2 = cv2.filter2D(thresh/size2/size2, -1, kernel_uniform)
        #ret,thresh2 = cv2.threshold(img2,255 * percent,255,cv2.THRESH_BINARY)
        # 5x5 with 5 weak signals should get removed
        ret,thresh = cv2.threshold(img,grey_threshold,255,cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        ret2,thresh2 = cv2.threshold(img, min(int(ret * 4 / 3), grey_threshold),255,cv2.THRESH_BINARY)

        #img3 = cv2.imread(os.path.join('binarized_canny', file), cv2.IMREAD_GRAYSCALE)
        img3 = cv2.imread(os.path.join('selected_images', folder, file), cv2.IMREAD_GRAYSCALE)
        blurred_img = cv2.GaussianBlur(img3, (5,5), 0)
        img3 = cv2.Canny(blurred_img, 20, 50)
        img3 = cv2.erode(cv2.dilate(img3, kernel_uniform, iterations=1), kernel_uniform, iterations=1)

        img5 = thresh2#cv2.erode(thresh2, kernel, iterations=1)# - thresh2
        raw_image = cv2.bitwise_and(img5, img3, img3)
        #raw_image = cv2.dilate(cv2.erode(raw_image, kernel2, iterations=1), kernel, iterations=1)

        #img7 = cv2.dilate(img5, kernel, iterations=2)
        #img8 = cv2.erode(img7, kernel, iterations=2)
        #final_image = raw_image
        count = 1
        num_iter = 0
        while(count > 0):
            diff = raw_image - cv2.erode(raw_image, kernel, iterations=1)
            count = 0
            num_iter += 1
            for x, y in zip(*np.nonzero(diff)):
                if not isErodable(x, y, raw_image):
                    continue
                raw_image[x][y] = 0
                count += 1
        #print(num_iter)
        #raw_image = cv2.erode(raw_image, kernel, iterations=1)
        #raw_image = cv2.dilate(raw_image, kernel, iterations=1)
        raw_image = cv2.dilate(raw_image, kernel, iterations=1)
        raw_image = cv2.erode(raw_image, kernel, iterations=1)

        cv2.imwrite(os.path.join(output, folder, file), raw_image)