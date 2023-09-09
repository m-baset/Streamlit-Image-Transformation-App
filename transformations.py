import numpy as np
from utils import linear_piecewise_mapping
import cv2

def piecewiseTransform(img, xp, yp):
  table = linear_piecewise_mapping(xp,yp)
  # Lookup table
  return cv2.LUT(img, table)

