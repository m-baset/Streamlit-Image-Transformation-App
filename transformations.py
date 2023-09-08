import numpy as np
from utils import linear_piecewise_mapping
import cv2

def contrastStreching(img, k, max_val, smooth):
  return max_val * ( 1 / (1 + np.exp(-((img.astype(np.float128)-int(k*max_val)) * smooth))))

def piecewiseTransform(img, xp, yp):
  table = linear_piecewise_mapping(xp,yp)
  # Lookup table
  return cv2.LUT(img, table)

