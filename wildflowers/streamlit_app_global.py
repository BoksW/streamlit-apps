import streamlit as st
import tensorflow as tf
import cv2
from PIL import Image

import urllib.request
import requests
import numpy as np

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.inception_v3 import preprocess_input


# Function for preprocessing
def preprocess_img(file):
    # Manually crop image to maintain aspect ratio before resizing with PIL
    # Cannot use keras.smart_resize as it has a bug that results in shifting of the image which results in adverse model performance
    with Image.open(file) as img:
        img = img.convert('RGB')
        ht = img.height
        w = img.width
        if w/ht > 1: # if width is longer, then crop along center of width
            new_w = ht
            left = (w - new_w) / 2
            right = left + new_w
            img = img.crop((left, 0, right, ht))
        else: # ht longer than width, crop along centre of width
            new_ht = w
            top = (ht - new_ht) / 2
            bottom = top + new_ht
            img = img.crop((0, top, w, bottom))

        # resize image with LANCZOS interpolation
        img = img.resize((299,299), Image.LANCZOS)

        # Convert image to array
        img_array = np.array(img)

        # pre-process (scale to -1,1)
        img_scaled = preprocess_input(img_array)

        # expand dimensions for input into model.predict
        return np.expand_dims(img_scaled, axis=0) # results in shape (1, 299, 299, 3)
    

# Function to interpret model results
def interpret_results(result):
    class_dict = {0: "Cupid's Shaving Brush",
                  1: 'Hairy Spurge',
                  2: 'Common Vernonia',
                  3: 'Lalang',
                  4: 'Prickly Lantana',
                  5: 'Touch-me-not',
                  6: 'Morning Glory',
                  7: 'Common Spiderwort',
                  8: 'Coat Buttons',
                  9: 'White Kyllinga'
                 }

    prediction = class_dict[result[0]]
    return prediction

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
        
                            

# load model, stored in cache for faster app run time
@st.cache_resource
def model_load():
    # load model locally
    url = '../model_2000/'
    model = tf.keras.models.load_model(url)
    return model

model = model_load()

# Title of webpage
st.title(":rainbow[A Wildflower Adventure]")

img_file = st.file_uploader(":black[Upload an image:]", type=['.jpg', '.jpeg'], help='Please upload single .jpg or .jpeg file')

st.divider()

if img_file is None:
    st.write(":blue[Awaiting image upload...]")

else:
    st.write(":blue[Uploaded image:]")

    # convert uploaded file to bytes       
    file_bytes = np.asarray(bytearray(img_file.read()), dtype=np.uint8)

    # decode and display image
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    st.image(img_rgb)

    # pre-process image
    sample = preprocess_img(img_file)
    
    # generate prediction
    result = np.argmax(model.predict(sample), axis=1)
    prediction = interpret_results(result)
    st.header(f":blue[Wildflower is likely to be '{prediction}']")
    st.write(f"Scientific name: {info[prediction]['Scientific name']}")
    st.write(f"Malay name: {info[prediction]['Malay name']}")
    st.write(f"Fun fact: {info[prediction]['Fun fact']}")

            


    