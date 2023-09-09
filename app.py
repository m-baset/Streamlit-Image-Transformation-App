import streamlit as st
import numpy as np
from utils import ReadImageFromURL, linear_piecewise_mapping, plot_and_save, plot_and_save_histogram
from transformations import *
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

st.title("Simple Photo Tweaker")

centered_container = st.empty()

#### Imaga URL Section ####
img_url = st.text_input("Enter Image Url")
if img_url:
    col1, col2 = st.columns(2)
    original_image = ReadImageFromURL(img_url=img_url, color="gray")
    plot_and_save_histogram(original_image, "before")
    col1.image(original_image, caption="Original Image")
    col2.image('img/before.png', caption="Original Image Histogram")

#### Select Transformation Section ####
transformations = ["Contrast Streching", "Piecewise Transformation", 
                   "Log Transform", "Inverse Log Transform", 
                   "Binary Threshold", "Negative", "Gamma Transform"]
transform_select = st.selectbox("Select one of the following point transformations", transformations)

#### Apply Transformation Section ####
if transform_select and img_url:

    #### Contrast Streching ####
    if transform_select == "Contrast Streching":

        ## Contrast Streching Parameters ##
        high = st.slider("High", 0, 255, step=1, value=255)
        low = st.slider("Low", 0, 255, step=1, value=0)
        
        ## Apply Contrast Strechtransformed_img = np.clip(transformed_img, 0, 1)ing ##
        cs_original_img = original_image.astype(np.float32) / 255.0
        transformed_img = ((cs_original_img - (low/255.0)) / ((high/255.0) - (low/255.0)))
        transformed_img = np.clip(transformed_img, 0, 1)
        transformed_img = (transformed_img * 255).astype(np.uint8)

        ## Plot transform function and histogram##
        x = np.arange(256)
        y = ((x - low) / (high - low)) * 255
        y = np.where((y >= 255), 255, y)
        y = np.where((y <= 0), 0, y)
        plot_and_save(x, y)
        plot_and_save_histogram(transformed_img, "after")

        ## Display Image After transformation and transform function ##
        st.write("Results:")
        col1, col2 = st.columns(2)
        col1.image(transformed_img/255, clamp=True, caption="Transformed Image")
        col2.image('img/transform.png', caption="Transformation Curve")
        st.image('img/after.png', caption="Transformed Image Histogram")

    #### Piecewise Transformation ####
    elif transform_select == "Piecewise Transformation":

        ## Transformation Parameters ##
        corner_points = st.slider("Number of corner points", 1, 5, step=1, value=3)
        if corner_points:
            col1, col2 = st.columns(2)
            xp = [0]
            yp = [0]
            for i in range(corner_points):
                x1 = col1.number_input(f"Point {i}", value=0)
                if x1 > 255:
                    x1 = 255
                elif x1 < 0:
                    x1 = 0
                xp.append(x1)

                x2 = col2.number_input(f"Point {i} mapping", value=0)
                if x2 > 255:
                    x2 = 255
                elif x2 < 0:
                    x2 = 0
                yp.append(x2)
            xp.append(255)
            yp.append(255)

            ## Plot transform function ##
            x = np.arange(256)
            plot_and_save(x, linear_piecewise_mapping(xp,yp))

            ## Apply Transformation ##
            transformed_img = piecewiseTransform(original_image, xp, yp)
            transformed_img = np.clip(transformed_img, 0, 255)
            plot_and_save_histogram(transformed_img, "after")

            ## Display Image After transformation and transform function ##
            st.write("Results:")
            col1, col2 = st.columns(2)
            col1.image(transformed_img/255, clamp=True, caption="Transformed Image")
            col2.image('img/transform.png', caption="Transformation Curve")
            st.image('img/after.png', caption="Transformed Image Histogram")

    #### Log Transform ####
    elif transform_select == "Log Transform":

        ## Log Transform Parameters ##
        c = 255 / np.log(1 + np.max(original_image))
        
        ## Plot transform function ##
        x = np.arange(256)
        plot_and_save(x, c * (np.log(x + 1)))

        ## Apply Transformation ##
        transformed_img = c * (np.log(original_image + 1))
        transformed_img = np.clip(transformed_img, 0, 255)
        plot_and_save_histogram(transformed_img, "after")
        
        ## Display Image After transformation and transform function ##
        st.write("Results:")
        col1, col2 = st.columns(2)
        col1.image(transformed_img/255, clamp=True, caption="Transformed Image")
        col2.image('img/transform.png', caption="Transformation Curve")
        st.image('img/after.png', caption="Transformed Image Histogram")

    #### Inverse Log Transform ####
    elif transform_select == "Inverse Log Transform":

        ## Inverse Log Transform Parameters ##
        c = 255 / np.log(1 + np.max(original_image))
        
        ## Plot transform function ##
        x = np.arange(256)
        plot_and_save(x, np.exp(x.astype(np. float128)) ** (1/c) - 1)

        ## Apply Transformation ##
        transformed_img = np.exp(original_image.astype(np. float128)) ** (1/c) - 1
        transformed_img = np.clip(transformed_img, 0, 255)
        plot_and_save_histogram(transformed_img, "after")

        ## Display Image After transformation and transform function ##
        st.write("Results:")
        col1, col2 = st.columns(2)
        col1.image(transformed_img/255, clamp=True, caption="Transformed Image")
        col2.image('img/transform.png', caption="Transformation Curve")
        st.image('img/after.png', caption="Transformed Image Histogram")

    #### Binary Threshold ####
    elif transform_select == "Binary Threshold":

        ## Thresholding Parameters ##
        k_thr = st.slider("K", 0, 255, step=1, value=128)

        ## Plot transform function ##
        x = np.arange(256)
        plot_and_save(x, np.where((x > k_thr), 255, 0))

        ## Apply Transformation ##
        transformed_img = np.where((original_image > k_thr), 255, 0)
        transformed_img = np.clip(transformed_img, 0, 255)
        plot_and_save_histogram(transformed_img, "after")

        ## Display Image After transformation and transform function ##
        st.write("Results:")
        col1, col2 = st.columns(2)
        col1.image(transformed_img/255, clamp=True, caption="Transformed Image")
        col2.image('img/transform.png', caption="Transformation Curve")
        st.image('img/after.png', caption="Transformed Image Histogram")

    #### Negative Transform ####
    elif transform_select == "Negative":
        
        ## Plot transform function ##
        x = np.arange(256)
        plot_and_save(x, 255 - x)

        ## Apply Transformation ##
        transformed_img = 255 - original_image
        transformed_img = np.clip(transformed_img, 0, 255)
        plot_and_save_histogram(transformed_img, "after")

        ## Display Image After transformation and transform function ##
        st.write("Results:")
        col1, col2 = st.columns(2)
        col1.image(transformed_img/255, clamp=True, caption="Transformed Image")
        col2.image('img/transform.png', caption="Transformation Curve")
        st.image('img/after.png', caption="Transformed Image Histogram")

    #### Gamma Transform ####
    elif transform_select == "Gamma Transform":

        ## Gamma Parameter ##
        gamma = st.slider("gamma", 0.1, 10.0, step=0.1, value=1.0)

        ## Plot transform function ##
        x = np.arange(256)
        x_gamma = np.power(x / 255.0, gamma) * 255.0 
        x_gamma = np.uint8(x_gamma)
        plot_and_save(x, x_gamma)

        ## Apply Transformation ##
        transformed_img = np.power(original_image / 255.0, gamma) * 255.0  
        transformed_img = np.uint8(transformed_img)
        transformed_img = np.clip(transformed_img, 0, 255)
        plot_and_save_histogram(transformed_img, "after")

        ## Display Image After transformation and transform function ##
        st.write("Results:")
        col1, col2 = st.columns(2)
        col1.image(transformed_img/255, clamp=True, caption="Transformed Image")
        col2.image('img/transform.png', caption="Transformation Curve"  )
        st.image('img/after.png', caption="Transformed Image Histogram")

    else:
        st.write("Not included Transformation")



