import matplotlib.pyplot as plt
import numpy as np
import cv2
import requests

def linear_piecewise_mapping(xp, yp):
    return np.interp(np.arange(256), xp, yp).astype('uint8')

def ReadImageFromURL(img_url, color="gray"):
    # Send an HTTP request to get the image content
    response = requests.get(img_url)
    image_data = response.content

    # Convert the image data to a NumPy array
    image_np_array = np.frombuffer(image_data, np.uint8)

    # Read the image using OpenCV
    if color == "gray":
        image = cv2.imdecode(image_np_array, cv2.IMREAD_GRAYSCALE)
    elif color == "rgb":
        image = cv2.imdecode(image_np_array, cv2.COLOR_BGR2RGB)

    return image

def plot_and_save(x_axis, y_axis):
    plt.plot(x_axis, y_axis)
    plt.xlabel("Input Pixel")
    plt.ylabel("Output Pixel")
    plt.title("Transformation Function")
    plt.savefig('img/transform.png')