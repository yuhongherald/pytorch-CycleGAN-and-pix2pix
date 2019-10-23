import os
import sys
import random
import tqdm
import shutil

train_p = 0.9
#val_p = 0.05
test_p = 0.05

root_dir = sys.argv[1]#"contoured-cut-outlines"
all_dir = sys.argv[2]#"all"
root_dir2 = sys.argv[3]
all_dir2 = sys.argv[4]
train_dir = "train"
val_dir = "val"
test_dir = "test"

def makepath(path):
    if not os.path.exists(path):
        os.mkdir(path)

if __name__ == "__main__":
    data = os.listdir(os.path.join(root_dir, all_dir))
    random.shuffle(data)
    total_count = len(data)
    train_split = int(train_p * total_count)
    test_split = int((1 - test_p) * total_count)
    train_data = data[:train_split]
    val_data = data[train_split:test_split]
    test_data = data[test_split:]

    makepath(os.path.join(root_dir, train_dir))
    makepath(os.path.join(root_dir2, train_dir))
    #newPath = shutil.copy("all/20063861.png", "test/20063861.png")
    for data in tqdm.tqdm(train_data, ascii=True, desc='train_data', unit='|image|'):
        newPath = shutil.copy(os.path.join(root_dir, all_dir, data), os.path.join(root_dir, train_dir, data))
        newPath = shutil.copy(os.path.join(root_dir2, all_dir2, data), os.path.join(root_dir2, train_dir, data))        

    makepath(os.path.join(root_dir, val_dir))
    makepath(os.path.join(root_dir2, val_dir))    
    for data in tqdm.tqdm(val_data, ascii=True, desc='val_data', unit='|image|'):
        newPath = shutil.copy(os.path.join(root_dir, all_dir, data), os.path.join(root_dir, val_dir, data))
        newPath = shutil.copy(os.path.join(root_dir2, all_dir2, data), os.path.join(root_dir2, val_dir, data))        

    makepath(os.path.join(root_dir, test_dir))
    makepath(os.path.join(root_dir2, test_dir))
    for data in tqdm.tqdm(test_data, ascii=True, desc='test_data', unit='|image|'):
        newPath = shutil.copy(os.path.join(root_dir, all_dir, data), os.path.join(root_dir, test_dir, data))
        newPath = shutil.copy(os.path.join(root_dir2, all_dir2, data), os.path.join(root_dir2, test_dir, data))        
