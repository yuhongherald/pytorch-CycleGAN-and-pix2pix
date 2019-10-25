import os.path
from data.base_dataset import BaseDataset, get_transform
from data.image_folder import make_dataset
from PIL import Image
import random
import csv
import torch
import numpy as np

class RoadshowDataset(BaseDataset):
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

        self.background_set = set()
        self.edge_set = set()
        self.class_dict = {}

        if opt.class_csv == 'None':
            return

        suffix = ['-b','']
        with open(self.dir_class) as file:
            input_file = csv.DictReader(file)
            for row in input_file:
                filename_var = row['filename'].lower()
                class_var = row['class'].lower()
                background_var = row['background'].lower()
                edge_var = row['edge'].lower()
                if background_var == 'yes':
                    self.background_set.add(filename_var)
                if edge_var == 'Photo':
                    self.edge_set.add(filename_var)
                    self.class_dict[filename_var] = class_to_int[class_var]

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
        B_path = self.B_paths[index]

        A_img = Image.open(A_path).convert('RGB')
        B_img = Image.open(B_path).convert('RGB')
        class_variable = torch.zeros([self.num_classes], dtype=torch.float32)

        filename = self.base_name[index].lower()

        class_index = self.class_dict.get(filename, 4) #, 4

        class_variable[class_index] = 1
        if filename in self.background_set:
            class_variable[self.num_classes - 2] = 1
        else:
            class_variable[self.num_classes - 2] = -1
        if filename in self.edge_set: #photo, weak edges included, like testA
            class_variable[self.num_classes - 1] = 1
        else:
            class_variable[self.num_classes - 1] = -1

        # apply image transformation
        A = self.transform_A(A_img)
        B = self.transform_B(B_img)

        return {'A': A, 'B': B, 'A_paths': A_path, 'B_paths': B_path, 'class_variable': class_variable}

    def __len__(self):
        """Return the total number of images in the dataset.

        As we have two datasets with potentially different number of images,
        we take a maximum of
        """
        return max(self.A_size, self.B_size)
