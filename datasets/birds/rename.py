import cv2
import numpy as np
import sys, os

input = sys.argv[1]
for image_name in os.listdir(input):
    if image_name[-4:].lower() != '.png' and image_name[-4:].lower() != '.jpg':
        continue
    image = cv2.imread(os.path.join(sub_dir1, image_name), -1)
    cv2.resize(
    old_name = os.path.join(input, image_name)
    os.rename(old_name, old_name[:-4] + "-b" + old_name[-4:])
