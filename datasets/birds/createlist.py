import csv
import os
import sys

folder = sys.argv[1]

with open(os.path.join(folder, 'class.csv'), 'w') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['filename','class']) #class
    for subfolder in (os.listdir(folder)):
        directory = os.path.join(folder, subfolder)
        if not os.path.isdir(directory):
            continue
        for file in (os.listdir(directory)):
            writer.writerow([file,subfolder])
