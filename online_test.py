from roadshow.gdrive import gdrive
from roadshow.image_parser import image_parser
import csv
import os
import cv2
import roadshow.resize
import numpy as np

class online_test:
    def __init__(self):
        self.file_id = '1Ubi4-MJflgn5J_5erkd7sZLNJxFwk93aZtSruOEWBUo'
        self.folder_id = '1grNv4nf5PbfdNb9NphMTGv9nme4R6Feq'
        self.ranges='Sheet!' #1:2 first 2 rows
        self.current_row = 2 #todo: make persistent
        self.num_columns = 6
        self.headers = ['Timestamp', 'Photo', 'class', 'name', 'Background', 'Image']
        self.csv_path = os.path.join('datasets', 'roadshow', 'class.csv')
        self.testA_path = 'datasets/roadshow/testA'
        self.testB_path = 'datasets/roadshow/testB'
        self.testA_cache_path = 'datasets/roadshow/testA_cache'
        self.testB_cache_path = 'datasets/roadshow/testB_cache'
        self.download_path = 'datasets/roadshow/downloads'
        self.results_path = 'datasets/roadshow/results'

        self.drive = gdrive('credentials.json', download_dir = self.download_path)
        self.parser = image_parser()

        try:
            if os.path.isfile(self.csv_path):
                os.unlink(self.csv_path)
            #elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)

        if not os.path.isfile(self.csv_path):
            with open(self.csv_path, 'w') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(['filename', 'class', 'background', 'edge'])

    def toEdges(self, image, type):
        if type == 'Photo':
            return self.parser.imagetoedge(image)
        else:
            return self.parser.binarize(image)

    def getAtt(self, image):
        return image.shape[0], image.shape[1]

    def createEmpty(self, image, padding):
        if len(image.shape) == 3:
            return np.full((256,256, 3), padding, dtype=np.uint8)
        else:
            return np.full((256,256), padding, dtype=np.uint8)

    def resize(self, base_img, padding):
        size = 256
        dimensions = base_img.shape
        max_dim = max(dimensions[0], dimensions[1])
        if (max_dim > size):
            base_img = cv2.resize(base_img,(int(dimensions[1] * size / max_dim), int(dimensions[0] * size / max_dim)), cv2.INTER_AREA)

        height, width = self.getAtt(base_img)
        x = height if height > width else width
        y = height if height > width else width
        square = self.createEmpty(base_img, padding)
        #
        #This does the job
        #
        square[int((y-height)/2):int(y-(y-height)/2), int((x-width)/2):int(x-(x-width)/2)] = base_img
        return square

    def clear(self, folder):
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                #elif os.path.isdir(file_path): shutil.rmtree(file_path)
            except Exception as e:
                print(e)

    def pollImages(self):
        #empty directory first
        self.clear('datasets/roadshow/testA')
        self.clear('datasets/roadshow/testB')
        data = []
        while len(data) == 0:
            self.drive.poll(self.file_id)
            self.current_row, data = self.drive.getData(self.file_id, self.current_row, self.num_columns)
            with open(self.csv_path, 'a') as csv_file:
                writer = csv.writer(csv_file)
                for row in data:
                    try:
                        id = row[5].split('id=', 1)[1]
                        filename = self.drive.download(id) #customize with name later
                        image = cv2.imread(os.path.join(self.download_path, filename), cv2.IMREAD_COLOR)
                        edges = self.resize(self.toEdges(image, row[1]), 0)
                        resized_image = self.resize(image, 255)
                        cv2.imwrite(os.path.join(self.testA_cache_path, filename), edges)
                        cv2.imwrite(os.path.join(self.testB_cache_path, filename), resized_image)
                        cv2.imwrite(os.path.join(self.testA_path, filename), edges)
                        cv2.imwrite(os.path.join(self.testB_path, filename), resized_image)
                        # write entry in csv file
                        writer.writerow([filename, row[2], row[4], row[1]])
                    except:
                        print('Failed to download image: ' + row[5])

    def uploadImages(self, save_paths):
        for save_path in save_paths:
            self.drive.upload(self.folder_id, save_path)

    def run(self):
        self.pollImages()
        # run the model
    
if __name__ == '__main__':
    test = online_test()
    #while True:
    #test.run()
    test.uploadImages(['./datasets/roadshow/result/163565451-b - edge 2birds.jpg'])
    #test.drive.listFiles()
