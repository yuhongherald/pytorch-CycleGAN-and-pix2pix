import os
import sys
import tqdm
import cv2
import numpy as np


# For each month
# For each subfolder
# Get filename from input folder
# Take file bechmark size from output

month_dir = "."
input_dir = "input"
output_dir = "background"
clean_dir = os.path.join("..", "clean")
size = 64

if __name__ == "__main__":
    month_folders = [name for name in os.listdir(month_dir) if os.path.isdir(os.path.join(month_dir, name))]
    for month in tqdm.tqdm(month_folders, ascii=True, desc='remove low resolution', unit='|month|'):
        submonth_dir = os.path.join(month_dir, month)
        submonth_folders = [name for name in os.listdir(submonth_dir) if os.path.isdir(os.path.join(submonth_dir, name))]
        
        subinput_dir = os.path.join(submonth_dir, input_dir)
        suboutput_dir = os.path.join(submonth_dir, output_dir)
        filenames = os.listdir(subinput_dir)
        for file in filenames:
            png_name = os.path.splitext(file)[0] + '.png'
            base_img = cv2.imread(os.path.join(suboutput_dir, png_name))
            width, height, channels = base_img.shape
            if (width < size or height < size):
                #print(os.path.join(suboutput_dir, png_name))
                continue
            
            for category in submonth_folders:
                final_name = png_name
                if category == input_dir:
                    final_name = file
                #shutil.copy('sample1.txt', '/home/varun/test')
                copy_img = cv2.imread(os.path.join(os.path.join(month, category, final_name)))
                cv2.imwrite(os.path.join(clean_dir, category, png_name), copy_img)
                #print(os.path.join(clean_dir, category, png_name))
