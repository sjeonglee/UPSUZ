import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

# image size로 분류
def is_rightsize(imgpath):
    img = cv.imread(imgpath)
    ratio = img.shape[1] / img.shape[0]
    if ratio > 0.99 and ratio < 1.01:
        return True
    else:
        return False

# road pixel로 분류
def is_enoughroad(imgpath, lower_p, upper_p):
    image = cv.imread(imgpath)
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    thresh = 0
    maxValue = 255
    th, dst = cv.threshold(gray, thresh, maxValue, cv.THRESH_BINARY)
    p = 1 - np.count_nonzero(dst) / (dst.shape[0] * dst.shape[1])
    if p > lower_p and p < upper_p:
        return True
    else:
        return False