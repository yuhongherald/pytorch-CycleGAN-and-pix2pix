import os.path
from data.base_dataset import BaseDataset, get_transform
from data.image_folder import make_dataset
from PIL import Image
import random
import csv
import torch
import numpy as np

class TwocatDataset(BaseDataset):
    """
    This dataset class can load unaligned/unpaired datasets.

    It requires two directories to host training images from domain A '/path/to/data/trainA'
    and from domain B '/path/to/data/trainB' respectively.
    You can train the model with the dataset flag '--dataroot /path/to/data'.
    Similarly, you need to prepare two directories:
    '/path/to/data/testA' and '/path/to/data/testB' during test time.
    """

    def __init__(self, opt):
        """Initialize this dataset class.

        Parameters:
            opt (Option class) -- stores all the experiment flags; needs to be a subclass of BaseOptions
        """
        BaseDataset.__init__(self, opt)
        self.dir_A = os.path.join(opt.dataroot, opt.phase + 'A')  # create a path '/path/to/data/trainA'
        self.dir_B = os.path.join(opt.dataroot, opt.phase + 'B')  # create a path '/path/to/data/trainB'
        self.dir_class = os.path.join(opt.dataroot, opt.class_csv)

        self.A_paths, _ = sorted(make_dataset(self.dir_A, opt.max_dataset_size))   # load images from '/path/to/data/trainA'
        self.B_paths, self.base_name = sorted(make_dataset(self.dir_B, opt.max_dataset_size))    # load images from '/path/to/data/trainB'

        self.A_size = len(self.A_paths)  # get the size of dataset A
        self.B_size = len(self.B_paths)  # get the size of dataset B
        btoA = self.opt.direction == 'BtoA'
        input_nc = self.opt.output_nc if btoA else self.opt.input_nc       # get the number of channels of input image
        output_nc = self.opt.input_nc if btoA else self.opt.output_nc      # get the number of channels of output image
        self.transform_A = get_transform(self.opt, grayscale=(input_nc == 1))
        self.transform_B = get_transform(self.opt, grayscale=(output_nc == 1))

        self.num_classes = opt.num_classes
        class_to_int = {
        'climbing': 0,
        'closeup': 1,
        'flying': 2,
        'interacting': 3,
        'perching': 4,
        'walking': 5
        }
        with open(self.dir_class) as file:
            input_file = csv.DictReader(open(file))
            self.class_dict = {}
            for row in input_file:
                self.class_dict[row['filename'].lower()] = class_to_int[row['class'].lower()]

    def __getitem__(self, index):
        """Return a data point and its metadata information.

        Parameters:
            index (int)      -- a random integer for data indexing

        Returns a dictionary that contains A, B, A_paths and B_paths
            A (tensor)       -- an image in the input domain
            B (tensor)       -- its corresponding image in the target domain
            A_paths (str)    -- image paths
            B_paths (str)    -- image paths
        """
        A_path = self.A_paths[index % self.A_size]  # make sure index is within then range
        #if self.opt.serial_batches:   # make sure index is within then range
        #    indexRandomA = index % self.A_size
        #    indexRandomB = index % self.A_size
        #else:
        #    indexRandomA = random.randint(0, self.A_size - 2)
        #    indexRandomB = random.randint(0, self.A_size - 2)
        #if indexRandomA == index:
        #    indexRandomA += 1
        #if indexRandomB == index:
        #    indexRandomB += 1
        B_path = self.B_paths[index]
        #randomA_path = self.A_paths[indexRandomA]
        #randomB_path = self.B_paths[indexRandomB]
        A_img = Image.open(A_path).convert('RGB')
        B_img = Image.open(B_path).convert('RGB')
        class_variable = torch.zeros([self.num_classes], dtype=torch.float32)

        class_index = self.class_dict.get(self.base_name[index].lower(), 4)
        random_class = np.random.randint(5)
        if random_class >= class_index:
            random_class += 1
        class_index = random_class
        #print(class_index)
        class_variable[class_index] = 1
        #randomA_img = Image.open(randomA_path).convert('RGB')
        #randomB_img = Image.open(randomB_path).convert('RGB')
        # apply image transformation
        A = self.transform_A(A_img)
        B = self.transform_B(B_img)
        #randomA = self.transform_A(randomA_img)
        #randomB = self.transform_B(randomB_img)

        return {'A': A, 'B': B, 'A_paths': A_path, 'B_paths': B_path, 'class_variable': class_variable}

    def __len__(self):
        """Return the total number of images in the dataset.

        As we have two datasets with potentially different number of images,
        we take a maximum of
        """
        return max(self.A_size, self.B_size)