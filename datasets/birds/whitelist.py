import csv
import os
import sys
import shutil

def rchop(thestring, ending):
    if thestring.endswith(ending):
        return thestring[:-len(ending)]
    return thestring

input_folder = sys.argv[1]
output_folder = sys.argv[2]
suffix = 'b'

file_set = set()
with open('whitelist.csv') as csv_file:
    input_file = csv.DictReader(csv_file)
    for row in input_file:
        file_set.add(row['filename'])


for file in os.listdir(input_folder):
    #print(file)
    if not rchop(os.path.splitext(file)[0], suffix) in file_set:
        continue
    shutil.copy(os.path.join(input_folder, file), output_folder)
