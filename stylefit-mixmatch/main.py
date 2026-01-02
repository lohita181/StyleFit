# # # main.py

# # import streamlit as st
# # import os
# # import pickle
# # import numpy as np
# # import tensorflow as tf
# # from PIL import Image
# # from tensorflow.keras.preprocessing import image
# # from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
# # from numpy.linalg import norm

# # # Create upload folders
# # os.makedirs("uploads/tops", exist_ok=True)
# # os.makedirs("uploads/bottoms", exist_ok=True)

# # # Load both models
# # top_model = tf.keras.models.load_model("top_classifier.keras")
# # bottom_model = tf.keras.models.load_model("bottom_classifier.keras")

# # # Load occasion labels
# # with open("top_labels.pkl", "rb") as f:
# #     top_labels = pickle.load(f)
# # with open("bottom_labels.pkl", "rb") as f:
# #     bottom_labels = pickle.load(f)

# # st.title("👚👖 Top & Bottom Fashion Recommender")

# # # Upload top images
# # top_files = st.file_uploader("📤 Upload TOP images", type=["jpg", "png", "jpeg"], accept_multiple_files=True, key="tops")
# # bottom_files = st.file_uploader("📥 Upload BOTTOM images", type=["jpg", "png", "jpeg"], accept_multiple_files=True, key="bottoms")

# # def predict_occasion(img_path, model, label_list):
# #     img = image.load_img(img_path, target_size=(224, 224))
# #     arr = image.img_to_array(img)
# #     arr = np.expand_dims(arr, axis=0)
# #     arr = preprocess_input(arr)
# #     predictions = model.predict(arr)[0]
# #     predicted_idx = np.argmax(predictions)
# #     return label_list[predicted_idx]

# # def save_file(uploaded_file, folder):
# #     path = os.path.join(folder, uploaded_file.name)
# #     with open(path, "wb") as f:
# #         f.write(uploaded_file.getbuffer())
# #     return path

# # if st.button("🎯 Predict and Match Outfits"):
# #     top_predictions = []
# #     bottom_predictions = []

# #     st.subheader("📸 Uploaded Tops")
# #     for file in top_files:
# #         path = save_file(file, "uploads/tops")
# #         label = predict_occasion(path, top_model, top_labels)
# #         top_predictions.append((path, label))
# #         st.image(path, caption=f"Predicted Occasion: {label}", width=150)

# #     st.subheader("👖 Uploaded Bottoms")
# #     for file in bottom_files:
# #         path = save_file(file, "uploads/bottoms")
# #         label = predict_occasion(path, bottom_model, bottom_labels)
# #         bottom_predictions.append((path, label))
# #         st.image(path, caption=f"Predicted Occasion: {label}", width=150)

# #     st.subheader("✨ Outfit Recommendations")
# #     for top_path, top_label in top_predictions:
# #         for bottom_path, bottom_label in bottom_predictions:
# #             if top_label == bottom_label:
# #                 st.write(f"🎯 Matched Occasion: {top_label}")
# #                 cols = st.columns(2)
# #                 cols[0].image(top_path, caption="Top")
# #                 cols[1].image(bottom_path, caption="Bottom")
# # main.py

# import streamlit as st
# import os
# import pickle
# import numpy as np
# import tensorflow as tf
# from PIL import Image
# from tensorflow.keras.preprocessing import image
# from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

# # Create upload folders
# os.makedirs("uploads/tops", exist_ok=True)
# os.makedirs("uploads/bottoms", exist_ok=True)

# # Load both models
# top_model = tf.keras.models.load_model("top_classifier.keras")
# bottom_model = tf.keras.models.load_model("bottom_classifier.keras")

# # Load occasion labels
# with open("top_labels.pkl", "rb") as f:
#     top_labels = pickle.load(f)
# with open("bottom_labels.pkl", "rb") as f:
#     bottom_labels = pickle.load(f)

# st.title("👚👖 Top & Bottom Fashion Recommender")

# # Upload top images
# top_files = st.file_uploader("📤 Upload TOP images", type=["jpg", "png", "jpeg"], accept_multiple_files=True, key="tops")
# bottom_files = st.file_uploader("📥 Upload BOTTOM images", type=["jpg", "png", "jpeg"], accept_multiple_files=True, key="bottoms")

# # Occasion selection dropdown
# all_occasions = list(set(top_labels) | set(bottom_labels))
# selected_occasion = st.selectbox("🎯 Select an Occasion to See Matched Outfits", all_occasions)

# def predict_occasion(img_path, model, label_list):
#     img = image.load_img(img_path, target_size=(224, 224))
#     arr = image.img_to_array(img)
#     arr = np.expand_dims(arr, axis=0)
#     arr = preprocess_input(arr)
#     predictions = model.predict(arr)[0]
#     predicted_idx = np.argmax(predictions)
#     return label_list[predicted_idx]

# def save_file(uploaded_file, folder):
#     path = os.path.join(folder, uploaded_file.name)
#     with open(path, "wb") as f:
#         f.write(uploaded_file.getbuffer())
#     return path

# if st.button("🎯 Predict and Match Outfits"):
#     top_predictions = []
#     bottom_predictions = []

#     st.subheader("📸 Uploaded Tops")
#     for file in top_files:
#         path = save_file(file, "uploads/tops")
#         label = predict_occasion(path, top_model, top_labels)
#         top_predictions.append((path, label))
#         st.image(path, caption=f"Predicted Occasion: {label}", width=150)

#     st.subheader("👖 Uploaded Bottoms")
#     for file in bottom_files:
#         path = save_file(file, "uploads/bottoms")
#         label = predict_occasion(path, bottom_model, bottom_labels)
#         bottom_predictions.append((path, label))
#         st.image(path, caption=f"Predicted Occasion: {label}", width=150)

#     st.subheader(f"✨ Outfit Recommendations for '{selected_occasion}'")
#     matched = False
#     for top_path, top_label in top_predictions:
#         for bottom_path, bottom_label in bottom_predictions:
#             if top_label == bottom_label == selected_occasion:
#                 matched = True
#                 st.write(f"🎯 Matched Occasion: {top_label}")
#                 cols = st.columns(2)
#                 cols[0].image(top_path, caption="Top")
#                 cols[1].image(bottom_path, caption="Bottom")

#     if not matched:
#         st.info(f"No matched outfits found for the occasion: {selected_occasion}")
# main.py

import streamlit as st
import os
import pickle
import numpy as np
import tensorflow as tf
from PIL import Image
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

# Create upload folders
os.makedirs("uploads/tops", exist_ok=True)
os.makedirs("uploads/bottoms", exist_ok=True)

# Load both models
top_model = tf.keras.models.load_model("top_classifier.keras")
bottom_model = tf.keras.models.load_model("bottom_classifier.keras")

# Load occasion labels
with open("top_labels.pkl", "rb") as f:
    top_labels = pickle.load(f)
with open("bottom_labels.pkl", "rb") as f:
    bottom_labels = pickle.load(f)

st.title("👚👖 Top & Bottom Fashion Recommender")

# Upload top images
top_files = st.file_uploader("📤 Upload TOP images", type=["jpg", "png", "jpeg"], accept_multiple_files=True, key="tops")
bottom_files = st.file_uploader("📥 Upload BOTTOM images", type=["jpg", "png", "jpeg"], accept_multiple_files=True, key="bottoms")

# Occasion selection dropdown
all_occasions = list(set(top_labels) | set(bottom_labels))
selected_occasion = st.selectbox("🎯 Select an Occasion to See Matched Outfits", all_occasions)

def predict_occasion(img_path, model, labels):
    print("dfd")
    img = image.load_img(img_path, target_size=(224, 224))
    arr = image.img_to_array(img)
    arr = np.expand_dims(arr, axis=0)
    arr = preprocess_input(arr)
    predictions = model.predict(arr)[0]
    predicted_index = np.argmax(predictions)
    predicted_label = labels[str(predicted_index)]
    print(f"{img_path} => {predictions}, index: {predicted_index}, label: {predicted_label}")
    return predicted_label

def save_file(uploaded_file, folder):
    path = os.path.join(folder, uploaded_file.name)
    with open(path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return path

def load_existing_predictions(folder, model, label_list):
    predictions = []
    for fname in os.listdir(folder):
        fpath = os.path.join(folder, fname)
        if os.path.isfile(fpath) and fname.lower().endswith(("jpg", "jpeg", "png")):
            label = predict_occasion(fpath, model, label_list)
            predictions.append((fpath, label))
    return predictions

if st.button("🎯 Predict and Match Outfits"):
    st.subheader("📸 Processing Uploaded Tops")
    for file in top_files:
        save_file(file, "uploads/tops")

    st.subheader("👖 Processing Uploaded Bottoms")
    for file in bottom_files:
        save_file(file, "uploads/bottoms")

    # Load and predict all tops and bottoms
    top_predictions = load_existing_predictions("uploads/tops", top_model, top_labels)
    bottom_predictions = load_existing_predictions("uploads/bottoms", bottom_model, bottom_labels)

    st.subheader(f"✨ Outfit Recommendations for '{selected_occasion}'")
    matched = False
    for top_path, top_label in top_predictions:
        for bottom_path, bottom_label in bottom_predictions:
            if top_label == bottom_label == selected_occasion:
                matched = True
                st.write(f"🎯 Matched Occasion: {top_label}")
                cols = st.columns(2)
                cols[0].image(top_path, caption="Top")
                cols[1].image(bottom_path, caption="Bottom")

    if not matched:
        st.info(f"No matched outfits found for the occasion: {selected_occasion}")

