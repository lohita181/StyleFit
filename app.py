from flask import Flask, render_template, request, redirect, url_for
import tensorflow as tf
import pickle
import os
import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join('static', 'uploads', 'tops')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
top_model = tf.keras.models.load_model("models/top_classifier.keras")
print("Top model loaded successfully")
bottom_model = tf.keras.models.load_model("models/bottom_classifier.keras")

with open("models/top_labels.pkl", "rb") as f:
    top_labels = pickle.load(f)
with open("models/bottom_labels.pkl", "rb") as f:
    bottom_labels = pickle.load(f)
occasion_mapping = {
    "workout": "sports wear",
    "adventure activities": "sports wear",
    "business meeting": "office wear",
    "graduation ceremony": "office wear",
    "summer vacation": "summer vacation",
    "birthday party": "birthday party"
}


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/topupload', methods=['GET', 'POST'])
def upload_top():
    if request.method == 'POST':
        files = request.files.getlist('top-upload')
        uploaded_urls = []
        for file in files:
            if file and allowed_file(file.filename):
                filename = file.filename
                save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(save_path)
                uploaded_urls.append(url_for('static', filename=f'uploads/tops/{filename}'))
        return render_template('topupload.html')
    return render_template('topupload.html')

@app.route('/upload-success')
def upload_success():
    return "File uploaded successfully!"

@app.route('/bottomupload', methods=['GET', 'POST'])
def upload_bottom():
    if request.method == 'POST':
        bottom_folder = os.path.join('static', 'uploads', 'bottoms')
        os.makedirs(bottom_folder, exist_ok=True)

        files = request.files.getlist('bottom-upload')
        uploaded_urls = []
        for file in files:
            if file and allowed_file(file.filename):
                filename = file.filename
                save_path = os.path.join(bottom_folder, filename)
                file.save(save_path)
                uploaded_urls.append(url_for('static', filename=f'uploads/bottoms/{filename}'))

        return render_template('bottomupload.html')
    return render_template('bottomupload.html')

@app.route('/occasion')
def occasion():
    return render_template('occasion.html')

def predict_occasion(img_path, model, labels):
    print("dfd")
    img = image.load_img(img_path, target_size=(224, 224))
    arr = image.img_to_array(img)
    arr = np.expand_dims(arr, axis=0)
    arr = preprocess_input(arr)
    predictions = model.predict(arr)[0]
    predicted_index = np.argmax(predictions)
    predicted_label = labels[predicted_index]
    print(f"{img_path} => {predictions}, index: {predicted_index}, label: {predicted_label}")
    return predicted_label

@app.route('/result', methods=['POST'])
def result():
    print(request.form.get("selected_occasion"))
    selected_occasion = request.form.get("selected_occasion")
    mapped_occasion = occasion_mapping.get(selected_occasion)

    top_dir = os.path.join("static", "uploads", "tops")
    bottom_dir = os.path.join("static", "uploads", "bottoms")

    top_predictions = []
    for filename in os.listdir(top_dir):
        if filename.lower().endswith(('jpg', 'jpeg', 'png')):
            path = os.path.join(top_dir, filename)
            label = predict_occasion(path, top_model, top_labels)
            top_predictions.append((path, label))

    bottom_predictions = []
    for filename in os.listdir(bottom_dir):
        if filename.lower().endswith(('jpg', 'jpeg', 'png')):
            path = os.path.join(bottom_dir, filename)
            label = predict_occasion(path, bottom_model, bottom_labels)
            bottom_predictions.append((path, label))
    print(f"Top model summary:{top_model.summary()}")
    print(f"bottom model summary:{bottom_model.summary()}")
    matched_outfits = []
    for top_img, top_label in top_predictions:
        for bottom_img, bottom_label in bottom_predictions:
            if top_label == bottom_label == mapped_occasion:
                matched_outfits.append((top_img, bottom_img))
    print(f"Matched Outfits: {matched_outfits}")  
    return render_template("result.html", occasion=selected_occasion, matched_outfits=matched_outfits)
if __name__ == "__main__":
    app.run(debug=True)