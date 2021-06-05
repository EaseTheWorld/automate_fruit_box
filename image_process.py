import cv2
import time
import numpy as np

def dump(matrix):
	for r in matrix:
		print(' ', r, ',')

use_max = True

if use_max:
	method = cv2.TM_CCOEFF_NORMED
else:
	method = cv2.TM_SQDIFF_NORMED

def find_image(src_png_buf, template_file, src_size):
	array_buf = np.frombuffer(src_png_buf, np.uint8)
	src_image = cv2.imdecode(array_buf, cv2.IMREAD_COLOR)
	# normalize OS display scaling
	if src_size:
		src_image = cv2.resize(src_image, src_size)
	template = cv2.imread(template_file)
	h, w = template.shape[:2]
	result = cv2.matchTemplate(src_image, template, cv2.TM_CCOEFF_NORMED)
	_, max_val, _, max_loc = cv2.minMaxLoc(result)
	if max_val > 0.90:
		return (max_loc[0], max_loc[1], max_loc[0]+w, max_loc[1]+h)
	else:
		return None


# Read the images from the file
def pattern_recognition(src_image, template, label, l, dst_image=None):
	h, w = template.shape[:2]
	
	result = cv2.matchTemplate(src_image, template, method)
	
	if use_max:
		threshold = 0.90
		max_val = 1
		while max_val > threshold:
		    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
		    if max_val > threshold:
		    	x,y = max_loc
		    	result[y-h//2:y+h//2+1, x-w//2:x+w//2+1] = 0
		    	l.append((y,x,label))
		    	if dst_image:
			    	cv2.rectangle(dst_image, (x,y), (x+w+1, y+h+1), (0,255,0))
			    	cv2.putText(dst_image, str(label), (x-5, y+10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 1)
		    	#print('x=', x, ' y=', y, ' val=', max_val)
	else:
		threshold = 0.05
		min_val = 0
		while min_val < threshold:
		    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)	
		    if min_val < threshold:
		    	x,y = min_loc
		    	result[y-h//2:y+h//2+1, x-w//2:x+w//2+1] = 1
		    	if dst_image:
			    	cv2.rectangle(dst_image, (x,y), (x+w+1, y+h+1), (0,255,0))
			    	cv2.putText(dst_image, str(label), (x-5, y+10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 1)
		    	#print('x=', x, ' y=', y, ' val=', min_val)

def offset_to_index(l, h, w):
	ly = sorted(l, key = lambda yxn : yxn[0])
	y_map = {}
	#print(ly)
	end_offset = -1
	y_idx = -1
	for yxn in ly:
		offset = yxn[0]
		if offset > end_offset:
			y_idx += 1
			start_offset = offset
			end_offset = start_offset + h
		y_map[offset] = y_idx
	
	lx = sorted(l, key = lambda yxn : yxn[1])
	x_map = {}
	#print(lx)
	end_offset = -1
	x_idx = -1
	for yxn in lx:
		offset = yxn[1]
		if offset > end_offset:
			x_idx += 1
			start_offset = offset
			end_offset = start_offset + w
		x_map[offset] = x_idx
	
	matrix = list([0] * (x_idx+1) for _ in range(y_idx+1))
	offset_matrix = list([0] * (x_idx+1) for _ in range(y_idx+1))
	for yxn in l:
		y_idx = y_map[yxn[0]]
		x_idx = x_map[yxn[1]]
		matrix[y_idx][x_idx] = yxn[2]
		offset_matrix[y_idx][x_idx] = (yxn[0], yxn[1], yxn[0]+h, yxn[1]+w)
	return (tuple(map(tuple, matrix)), tuple(map(tuple, offset_matrix)))

template_filelist = (
	('no1_32x30.png', 1),
	('no2_32x30.png', 2),
	('no3_32x30.png', 3),
	('no4_32x30.png', 4),
	('no5_32x30.png', 5),
	('no6_32x30.png', 6),
	('no7_32x30.png', 7),
	('no8_32x30.png', 8),
	('no9_32x30.png', 9)
)

marginY = 5
marginX = 7


#print(l)

#cv2.imwrite('output.png', dst_image)

#matrix = offset_to_index(l, h, w)

#dump(matrix)

def image_file_to_matrix(image_file):
	l = []
	h = 0
	w = 0
	src_image = cv2.imread(image_file)
	dst_image = cv2.imread(image_file)
	for template_file, label in template_filelist:
		template = cv2.imread(template_file)
		h, w = template.shape[:2]
		template = template[marginY:-marginY, marginX:-marginX]
		pattern_recognition(src_image, template, label, l)
	return offset_to_index(l, h, w)
