import streamlit as st
import os
import numpy as np
from PIL import Image,ImageEnhance
import numpy as np
from io import BytesIO
from PIL import ImageDraw
from streamlit_cropper import st_cropper


st.sidebar.title("🖼️ Image Tools App")
option=st.sidebar.radio("🔹 Navigate through tools:",[
        "🏠 Home","📏 Resize Image","✨ Enhance Image","✂️ Crop Image"
    ])

if option == '🏠 Home':

    st.title("✨Welcome to Image Tools App✨")
    st.subheader("Your one-stop solution for resizing, enhancing, and cropping images effortlessly")
    
    st.write("""
    🚀 **What you can do with this app:**
    - Resize images to exact dimensions in **cm**.
    - Enhance images (brightness, contrast, sharpness) in a click.
    - Crop images interactively.
    
    Use the sidebar to switch between different tools. 👈
    """)
    

    st.info("💡 Tip: Enter dimensions in **cm**; the app will automatically handle pixel conversion.")
    st.success("✅ Supported formats: JPG, JPEG, PNG, BMP, TIFF")
    

elif option=='📏 Resize Image':

    st.markdown("## 🎨 Resize Your Image Easily")
    st.markdown(
        "Upload your image and set the **width and height in cm**. "
        "The app will automatically convert it to pixels and resize your image."
    )
    st.markdown(
    "📌 **Example:** Let's say you want to convert an image to the size **3.5 cm × 4.5 cm**.\n\n"
    "- Here, **3.5 cm** is the **width**\n"
    "- And **4.5 cm** is the **height**\n\n"
    "Enter these values below and the app will resize your image accordingly!"
    )

    st.markdown("---")  # Horizontal line

    
    file=st.file_uploader("Select your image:",type=['jpg','jpeg','png','bmp','tiff', 'tif'])
    if file:
        filename=file.name
        extension=os.path.splitext(filename)[1].lower()

    with st.container(border=True):
        if file is not None:
            img = Image.open(file)
            img_array = np.array(img)

            st.write("🖼️ Original Image Shape (pixels):", img_array.shape)
            pixels_height = img_array.shape[0]
            pixels_width = img_array.shape[1]

            dpi=300

            width_inch = pixels_width / dpi
            height_inch = pixels_height / dpi

            width_cm = width_inch * 2.54
            height_cm = height_inch * 2.54

            st.write(f"Width in cm: {width_cm:.2f} cm")
            st.write(f"Height in cm: {height_cm:.2f} cm")
            

    t1=st.number_input("Enter width (cm):",min_value=1.0,step=1.0)
    t2=st.number_input("Enter height (cm):",min_value=1.0,step=1.0)

    dpi=300

    # Convert cm to pixels
    cm_to_inches = 0.393701
    width_px = int(t1 * cm_to_inches * dpi)
    height_px = int(t2 * cm_to_inches * dpi)

    if st.button("Resize an Image"):
        with st.container(border=True):
            col1,col2=st.columns(2)
            with col1:   
                img2=Image.open(file)
                st.image(img2, caption="Original", use_container_width=True)

            with col2:
                img = Image.open(file)
                size=(width_px,height_px) # size will be tuple now
                img_resized=img.resize(size, Image.LANCZOS)
                
                st.image(img_resized, caption="Resized", use_container_width=True)

                buffer = BytesIO()
                img_resized.save(buffer, format="JPEG", dpi=(dpi, dpi))  # Embed DPI if you want
                buffer.seek(0)  # Important: reset cursor

                st.download_button(
                    label="Download Resized Image",
                    data=buffer,
                    file_name="resized_image.jpeg",
                    mime=f"image/{extension}"
                )

elif option== '✨ Enhance Image':

    st.markdown("## ✨ Enhance Your Images in One Click")
    st.markdown("""
    Upload your image and click the 'Enhance Image' button.
    The app will automatically:
    - Increase sharpness
    - Improve brightness
    - Boost contrast
    """)    

    st.markdown("---")  # Horizontal line
    file=st.file_uploader("Select your image:",type=['jpg','jpeg','png','bmp','tiff', 'tif'])
    if file:
        filename=file.name
        extension=os.path.splitext(filename)[1].lower()
  
    if st.button("enhance an image"):

        with st.container(border=True):
            if file is not None:
                img = Image.open(file)
                img_array = np.array(img)

                st.write("🖼️ Original Image Shape (pixels):", img_array.shape)
                pixels_height = img_array.shape[0]
                pixels_width = img_array.shape[1]
                
                col1,col2=st.columns(2)
                with col1:   
                    img2=Image.open(file)
                    st.image(img2, caption="Original", use_container_width=True)

                with col2:
                    img = Image.open(file)
                    size=(pixels_width,pixels_height) # size will be tuple now
                    img_resize=img.resize(size, Image.LANCZOS)
                    enhancer = ImageEnhance.Sharpness(img_resize)
                    sharpened = enhancer.enhance(2.0)  # 1.0 = original, >1 = sharper

                    bright = ImageEnhance.Brightness(sharpened).enhance(1.1)  # >1 brighter

                    # Contrast
                    contrast = ImageEnhance.Contrast(bright).enhance(1.2)  # >1 higher contrast
                    
                    st.image(contrast, caption="Enhanced", use_container_width=True)

                    buffer=BytesIO()
                    contrast.save(buffer,format="JPEG")
                    buffer.seek(0)

                    st.download_button(
                        label="Download Enhanced Image",
                        data=buffer,
                        file_name="enhanced_image.jpeg",
                        mime=f"type/{extension}"
                    )

elif option=='✂️ Crop Image':


    st.title("📐 Interactive Image Cropper")
    st.write("Upload your image, then drag and select the part you want to keep.")
    st.info("💡 Tip: You can freely adjust the crop box or maintain an aspect ratio if needed.")

    st.markdown("---")  # Horizontal line
    file=st.file_uploader("Select your image:",type=['jpg','jpeg','png','bmp','tiff', 'tif'])
    if file:
        filename=file.name
        extension=os.path.splitext(filename)[1].lower()
    

    if file:
        img = Image.open(file)
        
        # Interactive cropper
        st.write("Drag and select the part of the image you want to keep.")
        cropped_img = st_cropper(
            img,
            realtime_update=True,   # updates crop in real-time
            box_color='blue',       # crop box color
            aspect_ratio=None       # None means free selection
        )

        # Show cropped image
        st.image(cropped_img, caption="Cropped Image", use_container_width=True)

        # Download cropped image
        buffer = BytesIO()
        cropped_img.save(buffer, format="JPEG")
        buffer.seek(0)
        st.download_button(
            label="Download Cropped Image",
            data=buffer,
            file_name="cropped_image.jpeg",
            mime=f"image/{extension}"
        )
