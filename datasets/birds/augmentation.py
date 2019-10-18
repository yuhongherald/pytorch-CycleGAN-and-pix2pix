import cv2
import numpy as np
import sys, os

"""
def transform(image):
	normalized = np.asarray(image, np.float32) / 255
	new_image = np.asarray(np.sqrt(normalized) * 255, np.uint8)
	return new_image

def autolevel(image):
	result = cv2.cvtColor(image, cv2.COLOR_BGR2HSV).copy()
	result[:, :, 2] = cv2.equalizeHist(result[:, :, 2])
	result = cv2.cvtColor(result, cv2.COLOR_HSV2BGR)

def get_edge(image):
	result = cv2.cvtColor(image, cv2.COLOR_BGR2HSV).copy()
	single_channel = np.asarray(np.asarray(result[:, :, 0], np.float32) * 2 / 3 + np.asarray(result[:, :, 1], np.float32) * 0 + np.asarray(result[:, :, 2], np.float32) / 3, np.uint8)
	edges1 = cv2.filter2D(single_channel, -1, direction1) + cv2.filter2D(single_channel, -1, direction1 * -1)
	edges2 = cv2.filter2D(single_channel, -1, direction1) + cv2.filter2D(single_channel, -1, direction1 * -1)
	edges = transform(edges1 + edges2)
	return edges
"""

def affine(images, paddings):
	#Parameters of the affine transform:
	angle = (np.random.rand() * 2 - 1) * 15 #Angle in degrees.
	shear = (np.random.rand() * 2 - 1) * 0.2
	tx = (np.random.rand() * 2 - 1) * images[0].shape[1] * 0.1
	ty = (np.random.rand() * 2 - 1) * images[0].shape[0] * 0.1

	type_border = cv2.BORDER_CONSTANT

	rows = images[0].shape[0]
	cols = images[0].shape[1]

	#First: Necessary space for the rotation
	M = cv2.getRotationMatrix2D((cols/2,rows/2), angle, 1)
	cos_part = np.abs(M[0, 0]); sin_part = np.abs(M[0, 1])
	new_cols = int((rows * sin_part) + (cols * cos_part))
	new_rows = int((rows * cos_part) + (cols * sin_part))

	#Second: Necessary space for the shear
	new_cols += (abs(shear)*new_cols+abs(tx))
	new_rows += (abs(shear)*new_rows+abs(ty))

	#Calculate the space to add with border
	up_down = int((new_rows-rows)/2); left_right = int((new_cols-cols)/2)

	results = []
	for image, padding in zip(images, paddings):
		color_border = (padding,padding,padding)
		final_image = cv2.copyMakeBorder(image, up_down, up_down,left_right,left_right,type_border, value = color_border)
		rows = final_image.shape[0]
		cols = final_image.shape[1]

		#Application of the affine transform.
		M_rot = cv2.getRotationMatrix2D((cols/2,rows/2),angle,1)
		translat_center_x = -(shear*cols)/2
		translat_center_y = -(shear*rows)/2

		M = M_rot + np.float64([[0,shear,tx + translat_center_x], [0,0,ty]])
		final_image  = cv2.warpAffine(final_image , M, (cols,rows),borderMode = type_border, borderValue = color_border)
		results.append(final_image)
	return results

def to3d(image):
	if len(image.shape) == 2:
		return np.expand_dims(image, axis=2)
	return image

def stretch_compress(images):
	is_y = int((np.sign(np.random.rand() - 0.5) + 1) / 2)
	area = int((0.05 + np.random.rand() * 0.05) * images[0].shape[is_y])
	stretch = int(np.random.rand() * (images[0].shape[is_y] - area * 2))
	compress = int(np.random.rand() * (images[0].shape[is_y] - area * 4))
	if compress >= stretch and compress <= stretch + area - 1:
		if compress + area * 3 < images[0].shape[is_y]:
			compress += area
		else:
			compress -= area * 3
	if compress + area * 2 >= stretch and compress + area * 2 <= stretch + area - 1:
		if compress - area >= 0:
			compress -= area
		else:
			compress += area * 3

	results = []
	for image in images:
		is_grey = len(image.shape) == 2
		image = to3d(image)
		if is_y == 0:
			image = np.transpose(image, [1, 0, 2])

		result = image.copy()
		f = 1 if compress > stretch else 0
		result[:, stretch:stretch+area * 2, :] = to3d(cv2.resize(image[:, stretch + (1-f) * area:stretch + (2-f) * area, :], (area * 2, image.shape[0])))
		result[:, compress + f * area:compress + (f+1) * area, :] = to3d(cv2.resize(image[:, compress:compress + area * 2, :], (area, image.shape[0])))
		start = stretch + area if f == 1 else compress + area * 2
		end = compress + 1 if f == 1 else stretch + area + 1
		g = f * 2 - 1
		result[:, start + g * area:end + g * area, :] = image[:, start:end, :]

		if is_y == 0:
			result = np.transpose(result, [1, 0, 2])
		if is_grey:
			result = np.squeeze(result, axis=2)
		results.append(result)
	return results

input = sys.argv[1]
edges = sys.argv[2]
output1 = sys.argv[3]
output2 = sys.argv[4]
for directory_name in ["train"]:#os.listdir(input):
	sub_dir1 = os.path.join(input, directory_name)
	sub_dir2 = os.path.join(edges, directory_name)
	if not os.path.isdir(sub_dir1):
		continue
	new_sub_dir1 = os.path.join(output1, directory_name)
	new_sub_dir2 = os.path.join(output2, directory_name)
	if not os.path.exists(new_sub_dir1):
		os.mkdir(new_sub_dir1)
	if not os.path.exists(new_sub_dir2):
		os.mkdir(new_sub_dir2)
	for image_name in os.listdir(sub_dir1):
		if image_name[-4:].lower() != '.jpg' and image_name[-4:].lower() != '.png':
			continue
		image = cv2.imread(os.path.join(sub_dir1, image_name), -1)
		edges = cv2.imread(os.path.join(sub_dir2, image_name[:-4] + '.jpg'), -1)
		for i in range(32):
			results = stretch_compress(affine([image, edges], [128, 0]))
            suffix = '____' + str(i).zfill(2)
			cv2.imwrite(os.path.join(new_sub_dir1, image_name[:-4] + str(i) + '.jpg'), results[0])
			cv2.imwrite(os.path.join(new_sub_dir2, image_name[:-4] + str(i) + '.jpg'), results[1])

