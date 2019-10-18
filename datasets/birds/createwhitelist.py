import csv
import os
import sys

def rchop(thestring, ending):
    if thestring.endswith(ending):
        return thestring[:-len(ending)]
    return None

folder = sys.argv[1]
suffix = '-b'

with open('whitelist.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['filename'])
    for file in (os.listdir(folder)):
        base_name, ext = os.path.splitext(file)
        base_name = rchop(base_name, suffix)
        if not base_name is None:
            writer.writerow([base_name]) #creates without -b and ext
