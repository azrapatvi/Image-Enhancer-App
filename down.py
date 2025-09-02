import streamlit as st
import numpy as np
from PIL import Image,ImageEnhance
import numpy as np
from io import BytesIO
from PIL import ImageDraw

file=st.file_uploader("Select your image:",type=['jpg','jpeg'])
with st.container(border=True):
    if file is not None:
        img = Image.open(file)
        img_array = np.array(img)

        st.write("Shape of Image:", img_array.shape)


t2=st.number_input("enter size of height:",min_value=1,step=1)
t1=st.number_input("enter size of width:",min_value=1,step=1)


if st.button("show image"):

    col1,col2=st.columns(2)
    with col1:   
        img2=Image.open(file)
        st.image(img2, caption="Original", use_container_width=True)

    with col2:
        img = Image.open(file)
        size=(t1,t2) # size will be tuple now
        img_resize=img.resize(size, Image.LANCZOS)
        enhancer = ImageEnhance.Sharpness(img_resize)
        sharpened = enhancer.enhance(2.0)  # 1.0 = original, >1 = sharper

        bright = ImageEnhance.Brightness(sharpened).enhance(1.1)  # >1 brighter

        # Contrast
        contrast = ImageEnhance.Contrast(bright).enhance(1.2)  # >1 higher contrast
        
        st.image(contrast, caption="Enhanced", use_container_width=True)

        buffer=BytesIO()
        img_resize.save(buffer,format="JPEG")
        buffer.seek(0)

        st.download_button(
            label="Download Enhanced Image",
            data=buffer,
            file_name="enhanced_image.jpeg",
            mime="type/jpeg"
        )


