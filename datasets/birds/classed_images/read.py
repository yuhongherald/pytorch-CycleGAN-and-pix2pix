import csv
import os

input_file = csv.DictReader(open('class.csv'))
class_dict = {}
for row in input_file:
    #class_dict[os.path.splitext(row['filename'])] = row['class'][0]
    print(row['class'])
