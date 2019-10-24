from roadshow.hed import hed
import cv2
import numpy as np

class image_parser:
    def __init__(self):
        #init HED model
        self.HED = hed()
        print('image parser init')
    def binarize(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        ret,thresh = cv2.threshold(image,128,255,cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        if len(np.nonzero(thresh)) > 0.5 * thresh.shape[0] * thresh.shape[1]:
            thresh = 255 - thresh
        return thresh
    def imagetoedge(self, image):
        return self.HED.imagetoedge(image)
    