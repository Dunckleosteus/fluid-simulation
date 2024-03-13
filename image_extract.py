from PIL import Image
import numpy as np
import os
import matplotlib.pyplot as plt

def get_obstacle():
    im = Image.open(os.path.join("profile_updated.png"))
    new_width = 300
    width_percent = (new_width / float(im.size[0]))
    new_height = int((float(im.size[1]) * float(width_percent)))

    resized_img = im.resize((new_width, new_height))
    # resized_img = resized_img.convert("L")

    np_img = np.array(resized_img)
    np_img = np_img[:, :, 2]
    print(np_img.shape)

    for x in range(np_img.shape[0]):
        for y in range(np_img.shape[1]):
            if np_img[x][y] != 15:
                np_img[x][y] = 0
    np_img[20:, :] = 15

    obstacle_array = np.full(np_img.shape, False) # if the value is false = empty space, else it's an obstacle
    for x in range(np_img.shape[0]):
        for y in range(np_img.shape[1]):
            if np_img[x][y] == 0:
                obstacle_array[x][y] = False
            else:
                obstacle_array[x][y] = True

    return obstacle_array
