import os
import sys
import tqdm
import cv2
import numpy as np

# For each outline
# If number of non-black pixels > 1%
# resize image
# Copy into subfolder threshold

clean_dir = os.path.join("..", "clean")
outline_dir = "outlines"
background_dir = "cut" #"background"
threshold_dir = "threshold"
threshold = 0.01
size = 64

if __name__ == "__main__":
    images = os.listdir(os.path.join(clean_dir, outline_dir))
    for image in tqdm.tqdm(images, ascii=True, desc='threshold', unit='|image|'):
        base_img = cv2.imread(os.path.join(os.path.join(clean_dir, outline_dir, image)))
        grey_img = cv2.cvtColor(base_img, cv2.COLOR_RGB2GRAY)

        width, height = grey_img.shape
        if cv2.countNonZero(grey_img) < threshold * width * height:
            continue

        rawImage = cv2.resize(base_img, (size, size), interpolation = cv2.INTER_AREA)
        cv2.imwrite(os.path.join(clean_dir, threshold_dir, outline_dir, image), rawImage)
        
        base_img2 = cv2.imread(os.path.join(os.path.join(clean_dir, background_dir, image)))
        rawImage2 = cv2.resize(base_img2, (size, size), interpolation = cv2.INTER_AREA)
        cv2.imwrite(os.path.join(clean_dir, threshold_dir, background_dir, image), rawImage2)
        
