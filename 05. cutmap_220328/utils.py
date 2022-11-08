# Setting Libraries

import numpy as np
import cv2 as cv
import os


# functions
def get_cities(data_dir: str):                         # get the name of the cities from the data folder
    folders = os.listdir(data_dir)
    return folders

def classify_pic(filename):                                 # check if the dominant color is white
    # Read pic
    img = cv.imread(filename)
    img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    
    # make copy and get dominant color
    img_temp = img.copy()
    unique, counts = np.unique(img_temp.reshape(-1, 3), axis=0, return_counts=True)
    img_temp[:,:,0], img_temp[:,:,1], img_temp[:,:,2] = unique[np.argmax(counts)]
    
    return np.array_equal(img_temp[0, 0], np.array([255, 255, 255]))