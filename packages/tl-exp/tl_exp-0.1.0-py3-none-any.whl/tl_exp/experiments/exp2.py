!pip install kagglehub


import kagglehub

# Download the dataset
path = kagglehub.dataset_download("antobenedetti/animals")

# Check the path to the dataset files
print("Path to dataset files:", path)


import os

# List all files in the dataset folder
dataset_path = '/root/.cache/kagglehub/datasets/antobenedetti/animals/versions/5'
dataset_files = os.listdir(dataset_path)
print("Files in the dataset:", dataset_files)


import os

# Path to the dataset directory
dataset_path = '/root/.cache/kagglehub/datasets/antobenedetti/animals/versions/5'

# List all files and directories in the dataset folder
dataset_files = os.listdir(dataset_path)

# Print the dataset files to inspect the structure
print("Dataset files and subdirectories:")
for file in dataset_files:
    print(file)


import os

# Path to the 'animals' subdirectory
animals_path = os.path.join(dataset_path, 'animals')

# List all files in the 'animals' directory
animals_files = os.listdir(animals_path)

# Print the contents of the 'animals' directory
print("Files in the 'animals' directory:")
for file in animals_files:
    print(file)


# List the contents of the 'val', 'inf', and 'train' subdirectories
subdirs = ['val', 'inf', 'train']

for subdir in subdirs:
    subdir_path = os.path.join(animals_path, subdir)

    # List files in the current subdirectory
    subdir_files = os.listdir(subdir_path)

    # Print the contents of the subdirectory
    print(f"\nFiles in the '{subdir}' directory:")
    for file in subdir_files:
        print(file)


import os
from PIL import Image
import matplotlib.pyplot as plt

# Path to the 'inf' directory which contains images
inf_path = os.path.join(animals_path, 'inf')

# List all image files in the 'inf' directory
image_files = [f for f in os.listdir(inf_path) if f.endswith('.jpg') or f.endswith('.png')]

# Check if there are image files
if len(image_files) > 0:
    # Display the first 5 images (you can adjust the range as needed)
    plt.figure(figsize=(15, 15))  # Adjust the figure size to make it easier to view multiple images

    for i, image_file in enumerate(image_files[:5]):
        image_path = os.path.join(inf_path, image_file)

        # Open the image
        img = Image.open(image_path)

        # Display the image using matplotlib
        plt.subplot(1, 5, i + 1)  # Create a subplot for each image
        plt.imshow(img)
        plt.axis('off')  # Hide axis
        plt.title(f"Image {i + 1}")

    plt.show()
else:
    print("No image files found in the 'inf' directory.")


import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, GlobalAveragePooling2D
from keras.applications import VGG16
from keras.preprocessing import image
from keras.utils import image_dataset_from_directory
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import os

dataset_path = '/root/.cache/kagglehub/datasets/antobenedetti/animals/versions/5/animals'
print("Files:", os.listdir(dataset_path))

# Directories for training and validation
train_dir = os.path.join(dataset_path, 'train')
val_dir = os.path.join(dataset_path, 'val')

# Load datasets
train_dataset = image_dataset_from_directory(train_dir, image_size=(128, 128), batch_size=32)
val_dataset = image_dataset_from_directory(val_dir, image_size=(128, 128), batch_size=32)

# Get class names
class_names = train_dataset.class_names
print("\nClass names:", class_names)

train_count = sum([len(batch[0]) for batch in train_dataset])
val_count = sum([len(batch[0]) for batch in val_dataset])
print(f"\nTotal training images: {train_count}")
print(f"Total validation images: {val_count}")

# Count number of images per class in the training dataset
class_counts = [0] * len(class_names)
for _, labels in train_dataset.unbatch():
    class_counts[int(labels.numpy())] += 1

# Plot histogram
plt.figure(figsize=(10, 6))
plt.bar(class_names, class_counts, color='skyblue')
plt.xticks(rotation=45)
plt.xlabel("Animal Class")
plt.ylabel("Number of Images")
plt.title("Number of Images per Class in Training Dataset")
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 10))
for images, labels in train_dataset.take(1):
    for i in range(9):
        ax = plt.subplot(3, 3, i + 1)
        plt.imshow(images[i].numpy().astype("uint8"))
        plt.title(f"Label: {class_names[labels[i]]}")
        plt.axis("off")

normalization_layer = keras.layers.Rescaling(1./255)
train_dataset = train_dataset.map(lambda x, y: (normalization_layer(x), y))
val_dataset = val_dataset.map(lambda x, y: (normalization_layer(x), y))

# Load VGG16 base model (without the top classifier layers)
vgg_base = VGG16(weights='imagenet', include_top=False, input_shape=(128, 128, 3))
vgg_base.trainable = False  # Freeze convolutional base

model = Sequential([
    vgg_base,
    GlobalAveragePooling2D(),
    Dense(256, activation='relu'),
    Dropout(0.5),
    Dense(len(class_names), activation='softmax')  # Output layer
])

# Compile model
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model.summary()

# Train the model
logs = model.fit(train_dataset, epochs=2, validation_data=val_dataset)

# Plot accuracy/loss
plt.figure(figsize=(8, 4))
plt.subplot(1, 2, 1)
plt.plot(logs.history['accuracy'], label='Train Acc')
plt.plot(logs.history['val_accuracy'], label='Val Acc')
plt.title('Accuracy')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(logs.history['loss'], label='Train Loss')
plt.plot(logs.history['val_loss'], label='Val Loss')
plt.title('Loss')
plt.legend()
plt.tight_layout()
plt.show()

res = model.evaluate(val_dataset)
print(f"\nTest Accuracy: {res[1]:.4f}")

# Prediction and Confusion Matrix
y_true = []
y_pred = []

for images, labels in val_dataset:
    preds = model.predict(images)
    y_pred.extend(np.argmax(preds, axis=1))
    y_true.extend(labels.numpy())

y_true = np.array(y_true)
y_pred = np.array(y_pred)


cm = confusion_matrix(y_true, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=class_names)
disp.plot(cmap=plt.cm.Blues)
plt.title("Confusion Matrix")
plt.show()

