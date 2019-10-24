from roadshow.gdrive import gdrive
from roadshow.image_parser import image_parser
import csv
import os
import cv2
import roadshow.resize
import numpy as np

class online_test:
    def __init__(self):
        self.drive = gdrive('credentials.json')
        self.parser = image_parser()
        self.file_id='1Ubi4-MJflgn5J_5erkd7sZLNJxFwk93aZtSruOEWBUo'
        self.ranges='Sheet!' #1:2 first 2 rows
        self.current_row = 2
        self.num_columns = 6
        self.headers = ['Timestamp', 'Photo', 'class', 'name', 'Background', 'Image']

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

    def pollImages(self):
        #self.drive.poll(self.file_id)
        current_row, data = self.drive.getData(self.file_id, self.current_row, self.num_columns)
        with open(os.path.join('datasets', 'roadshow', 'class.csv'), 'w') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['filename', 'class', 'background', 'edge'])
            for row in data:
                id = row[5].split('id=', 1)[1]
                print(id)
                filename = self.drive.download(id) #customize with name later
                image = cv2.imread('datasets/roadshow/download' + '/' + filename)
                edges = self.resize(self.toEdges(image, row[1]), 0)
                resized_image = self.resize(image, 255)
                cv2.imwrite('datasets/roadshow/testA' + '/' + filename, edges)
                cv2.imwrite('datasets/roadshow/testB' + '/' + filename, resized_image)
                # write entry in csv file
                writer.writerow([filename, row[3], row[4], row[1]])

    def run(self):
        self.pollImages()
        # run the model
    
if __name__ == '__main__':
    test = online_test()
    #while True:
    test.run()