import os
import sys
import tqdm
import csv
import shutil

input_dir = sys.argv[1]
output_dir = sys.argv[2]

fileset = set()

with open('files.csv') as file:
    input_file = csv.DictReader(file)
    for row in input_file:
        fileset.add(row['filename'])

for folder in os.listdir(input_dir):
    if not os.path.isdir(os.path.join(input_dir, folder)):
        continue
    path = os.path.join(input_dir, folder)
    outpath = os.path.join(output_dir, folder)
    if not os.path.exists(outpath):
        os.mkdir(outpath)
    for file in tqdm.tqdm(os.listdir(path), ascii=True, desc='resize images', unit='|image|'):
        filename, ext = os.path.splitext(file)
        if not (filename in fileset):
            continue
        shutil.copy(os.path.join(path, file), os.path.join(output_dir, folder, file))