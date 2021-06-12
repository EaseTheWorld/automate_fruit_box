import cv2
import time
import numpy as np

def dump(matrix):
	for r in matrix:
		print(' '.join(map(lambda x : ' ' if x == 0 else str(x), r)))

class Node:
    def __init__(self, y, x, h, w, label, confidence):
        self.y = y
        self.x = x
        self.h = h
        self.w = w
        self.label = label
        self.confidence = confidence

    def get_label(self):
        return self.label

    def get_rect(self):
        return (self.y, self.x, self.y+self.h, self.x+self.w)

    def dump(self):
        return (self.label, self.confidence, self.y, self.x)

def save_image_with_size(src_png_buf, target_size, target_file):
    array_buf = np.frombuffer(src_png_buf, np.uint8)
    src_image = cv2.imdecode(array_buf, cv2.IMREAD_COLOR)
    src_image = cv2.resize(src_image, target_size)
    cv2.imwrite(target_file, src_image)

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


def pattern_recognition(src_image, template, label, dst_image=None):
    node_list = []
    h, w = template.shape[:2]

    result = cv2.matchTemplate(src_image, template, cv2.TM_CCOEFF_NORMED)

    threshold = 0.90
    max_val = 1
    while max_val > threshold:
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        if max_val > threshold:
            x,y = max_loc
            result[y-h//2:y+h//2+1, x-w//2:x+w//2+1] = 0
            node_list.append(Node(y,x,h,w,label,max_val))
            if dst_image:
                cv2.rectangle(dst_image, (x,y), (x+w+1, y+h+1), (0,255,0))
                cv2.putText(dst_image, str(label), (x-5, y+10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 1)
    return node_list

def get_node_matrix(l):
    y_map = {}
    end_offset = -1
    y_idx = -1
    for node in sorted(l, key = lambda node : node.y):
        if node.y > end_offset:
            y_idx += 1
            start_offset = node.y
            end_offset = start_offset + node.h
        y_map[node.y] = y_idx

    x_map = {}
    end_offset = -1
    x_idx = -1
    for node in sorted(l, key = lambda node : node.x):
        if node.x > end_offset:
            x_idx += 1
            start_offset = node.x
            end_offset = start_offset + node.w
        x_map[node.x] = x_idx

    node_matrix = list([None] * (x_idx+1) for _ in range(y_idx+1))
    for node in l:
        y_idx = y_map[node.y]
        x_idx = x_map[node.x]
        #if node_matrix[y_idx][x_idx]:
            #print('y=', y_idx, 'x=', x_idx, 'confusing', node_matrix[y_idx][x_idx].dump(), node.dump())
        if not node_matrix[y_idx][x_idx] or node.confidence > node_matrix[y_idx][x_idx].confidence:
            node_matrix[y_idx][x_idx] = node
    return node_matrix

#print(l)

#cv2.imwrite('output.png', dst_image)

#matrix = offset_to_index(l, h, w)

#dump(matrix)

def image_file_to_matrix(image_file, template_filelist):
    node_list = []
    src_image = cv2.imread(image_file)
    #dst_image = cv2.imread(image_file)

    for template_file, label in template_filelist:
        template = cv2.imread(template_file)
        node_list += pattern_recognition(src_image, template, label)

    node_matrix = get_node_matrix(node_list)
    label_matrix = tuple(tuple(map(Node.get_label, row)) for row in node_matrix)
    rect_matrix = tuple(tuple(map(Node.get_rect, row)) for row in node_matrix)
    return label_matrix, rect_matrix
