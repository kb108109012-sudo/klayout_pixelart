import cv2 as cv
import numpy as np
import glob
import os

img_folder = "assets/gengar"
img_paths = glob.glob(f"{img_folder}/*.*")

colors = np.array([
    [92,76,156], # shadow blue
    [148, 116, 180], # gengar colors
    [180, 141, 118],  # gengar body colors
    [255, 255, 255],  # white
    [252, 92, 92],   # red
    [0, 0, 0]        # black
])

def dist_calc(pixel, colors):

    dist = np.zeros(colors.shape[0])
    for i in range(colors.shape[0]):
        #print(f"pixel {pixel} color: {colors[i]}")
        d = abs(pixel - colors[i])
        d = np.sum(d)
        #print(d)
        dist[i] = d

    return np.argmin(dist)

def color_quant(colors, img):
    shape_x, shape_y, pixel_size = img.shape
    q_img = np.zeros([shape_x, shape_y])
    #print(f"shape x: {shape_x} y: {shape_y}")
    for i in range(shape_x):
        for j in range(shape_y):
            #print(f"i: {i} j: {j}")
            q_img[i][j] = dist_calc(img[i][j], colors)
    
    return q_img

### write to a file
def write_to_file(img, filename):
    rows = img.shape[0]
    img_merged = []
    with open(f"{filename}", "w") as f:
        for i in range(rows):
            #print(f"i: {i}")
            row_val = img[i].astype(str)
            row_str = ' '.join(row_val)
            #print(row_str)
            img_merged = row_str
            f.write(img_merged)
            f.write("\n")
    f.close()

for img_path in img_paths:

    filename = os.path.basename(img_path)
    name_only = os.path.splitext(filename)[0]
    print(f"Reading the image file: {img_path}")

    img = cv.imread(img_path)
    rgb_img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    resized_img = cv.resize(rgb_img, (200, 200), interpolation=cv.INTER_AREA)

    arr = np.array(resized_img)
    mapped_img = color_quant(colors, arr).astype(int)
    print(mapped_img.shape)
    write_to_file(mapped_img, f"mapped_output/{name_only}.txt")
    print(f"Writing the mapped output to the file: mapped_output/{name_only}.txt")
