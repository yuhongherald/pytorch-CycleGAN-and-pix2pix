import cv2

def resize(size, padding):
    dimensions = base_img.shape
    max_dim = max(dimensions[0], dimensions[1])
    if (max_dim > size):
        base_img = cv2.resize(base_img,(int(dimensions[1] * size / max_dim), int(dimensions[0] * size / max_dim)), cv2.INTER_AREA)

    height, width, channels = base_img.shape
    x = height if height > width else width
    y = height if height > width else width
    square= np.full((size,size,3), padding, dtype=np.uint8)
    #
    #This does the job
    #
    square[int((y-height)/2):int(y-(y-height)/2), int((x-width)/2):int(x-(x-width)/2)] = base_img
    return square