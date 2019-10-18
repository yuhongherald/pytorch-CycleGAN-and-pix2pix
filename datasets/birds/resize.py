import os
import sys
import tqdm
import cv2
import numpy as np

input_dir = sys.argv[1]
output_dir = sys.argv[2]
padding = sys.argv[3]
size = 256

for folder in os.listdir(input_dir):
    if not os.path.isdir(os.path.join(input_dir, folder)):
        continue
    path = os.path.join(input_dir, folder)
    outpath = os.path.join(output_dir, folder)
    if not os.path.exists(outpath):
        os.mkdir(outpath)
    for file in tqdm.tqdm(os.listdir(path), ascii=True, desc='resize images', unit='|image|'):
        base_img = cv2.imread(os.path.join(path, file))
        dimensions = base_img.shape
        max_dim = max(dimensions[0], dimensions[1])
        if (max_dim > size):
            base_img = cv2.resize(base_img,(int(dimensions[1] * size / max_dim), int(dimensions[0] * size / max_dim)), cv2.INTER_AREA)

        height, width, channels = base_img.shape
        x = height if height > width else width
        y = height if height > width else width
        square= np.full((size,size,3), padding, dtype=np.uint8)
        #
        #This does the job
        #
        square[int((y-height)/2):int(y-(y-height)/2), int((x-width)/2):int(x-(x-width)/2)] = base_img
        # resized_img = cv2.resize(square, (size, size))
        cv2.imwrite(os.path.join(output_dir, folder, file), square)    
