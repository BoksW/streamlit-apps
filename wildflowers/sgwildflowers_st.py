import streamlit as st
from PIL import Image
from PIL import ExifTags
import requests
import os
import io
import numpy as np


# Dictionary of information
info = {"Cupid's Shaving Brush": {"Scientific name": "Emilia sonchifolia",
                                  "Malay name": "Ketumbit Jantan",
                                  "Fun fact": "My other name is 'lilac tasselflower'. I look very much like the Common Vernonia, but my flowers are longer and look like a vase!"},
        "Hairy Spurge": {"Scientific name": "Euphorbia hirta",
                         "Malay name": "Ara Tanah (which means 'ground fig')",
                         "Fun fact": "I have medicinal properties - I can be used to treat gastrointestinal (tummy) issues, asthma and bronchitis (lung infection)!"},
        "Common Vernonia": {"Scientific name": "Vernonia cinerea",
                            "Malay name": "Rumput Tahi Babi (which means 'Pig dung grass', ew!) / Rumput Sepagi (which means morning grass, that sounds better..)",
                            "Fun fact": "My other name is 'Little Ironweed' - my flowers change into white fluffy tufts! Huff and puff on these white tufts and help my seeds fly away!"},
        "Lalang": {"Scientific name": "Imperata cylindrica",
                   "Malay name": "Lalang (which literally means 'weeds')!",
                   "Fun fact": "I can grow up to 180 centimeters tall (that's probably taller than your Dad)!"},
        "Prickly Lantana": {"Scientific name": "Lantana camara",
                   "Malay name": "Bunga Tahi Ayam (which means 'chicken poop flower')",
                   "Fun fact": "I may look very pretty, and my berries may look yummy, but please don't eat my as I am poisonous!"},
        "Touch-me-not": {"Scientific name": "Mimosa pudica",
                        "Malay name": "Malu-malu (which means 'shy')",
                        "Fun fact": "I am really shy, touch my leaves and watch them close up!"},
        "Morning Glory": {"Scientific name": "Ipomoea cairica",
                          "Malay name": "None",
                          "Fun fact": "I'm a creeping plant, so you'll usually find me climbing up fences!"},
        "Common Spiderwort": {"Scientific name": "Commelina diffusa",
                              "Malay name": "Rumput aur (which means 'golden grass')",
                              "Fun fact": "My leaves are rich in Vitamin C - early settlers in Australia consumed this plant to prevent scurvy (a disease caused by a lack of Vitamin C)"},       
        "Coat Buttons":{"Scientific name": "Tridax procumbens",
                        "Malay name": "Kanching Baju",
                        "Fun fact": "I can be used as rabbit food!"},
        "White Kyllinga":{"Scientific name": "Cyperus mindorensis",
                          "Malay name": "None",
                          "Fun fact": "I grow via a long rhizome (underground horizontal stem), and a decoction of these rhizomes may be used to treat fever!"}
       }
        
                            
# Google cloud run API URL
API_URL = 'https://sgwildflowers-6vgyceft2q-as.a.run.app/predict'

# Title of webpage
st.title(":rainbow[A Wildflower Adventure]")

img_file = st.file_uploader(":black[Upload an image:]", type=['.jpg', '.jpeg'], help='Please upload single .jpg or .jpeg file')

st.divider()

if img_file is None:
    st.write(":blue[Awaiting image upload...]")

else:
    st.write(":blue[Uploaded image:]")

    # read file once and store this as variable
    file_data = img_file.read()

    # Display image using PIL
    pil_img = Image.open(io.BytesIO(file_data))

    # Check and correct image orientation
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
                # orientation variable now contains the numerical ID of the 'Orientation' tag
        exif = dict(pil_img._getexif().items())

        if exif[orientation] == 3:
            pil_img = pil_img.rotate(180, expand=True)
        if exif[orientation] == 6:
            pil_img = pil_img.rotate(270, expand=True)
        if exif[orientation] == 8:
            pil_img = pil_img.rotate(90, expand=True)
    except (AttributeError, KeyError, IndexError):
        # cases where the image doesn't have EXIF info
        pass
    
    st.image(pil_img)
    
    # send image data to the API
    response = requests.post(API_URL, files={'file': ('image.jpg', file_data)})
    
    try:
        prediction = response.text
        st.header(f":blue[Wildflower is likely to be '{prediction}']")
        st.write(f"Scientific name: {info[prediction]['Scientific name']}")
        st.write(f"Malay name: {info[prediction]['Malay name']}")
        st.write(f"Fun fact: {info[prediction]['Fun fact']}")
    except Exception as e:
        st.write(f'Error processing API response: {e}')

        

            


    