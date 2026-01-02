# train_top_or_bottom_model.py

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import os
import pickle

dataset_path = "bottoms"  # or "bottoms"

# Data augmentation
train_datagen = keras.preprocessing.image.ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)

train_dataset = train_datagen.flow_from_directory(
    dataset_path,
    target_size=(224, 224),
    batch_size=16,
    class_mode='sparse',
    shuffle=True
)

occasion_labels = list(train_dataset.class_indices.keys())
print("✅ Detected occasions:", occasion_labels)

# Load base model
base_model = keras.applications.MobileNetV2(
    input_shape=(224, 224, 3),
    include_top=False,
    weights='imagenet'
)
base_model.trainable = False

# Define model
model = keras.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.3),
    layers.Dense(len(occasion_labels), activation='softmax')
])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(train_dataset, epochs=10)

# Save the model and labels
model_name = "top_classifier.keras" if "top" in dataset_path else "bottom_classifier.keras"
labels_name = "top_labels.pkl" if "top" in dataset_path else "bottom_labels.pkl"

model.save(model_name)
with open(labels_name, "wb") as f:
    pickle.dump(occasion_labels, f)

print(f"✅ Model saved as {model_name}")
print(f"✅ Labels saved as {labels_name}")
