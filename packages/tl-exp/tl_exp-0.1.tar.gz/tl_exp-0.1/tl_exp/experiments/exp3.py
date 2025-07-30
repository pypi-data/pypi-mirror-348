import keras
from keras.applications import VGG16
from keras import models
from keras import layers


conv_base = VGG16(weights='imagenet',include_top=False,input_shape=(224, 224, 3))

conv_base.summary()

for layer in conv_base.layers:
  print(layer.name,layer.trainable)

import tensorflow as tf
from tensorflow.keras.datasets import cifar10
from tensorflow.keras.utils import to_categorical
import cv2
import numpy as np
import matplotlib.pyplot as plt

(x_train, y_train), (x_test, y_test) = cifar10.load_data()
y_train_onehot = to_categorical(y_train, 10)
y_test_onehot = to_categorical(y_test, 10)


import collections

# Count samples per class in training set
train_labels_flat = y_train.flatten()
counter = collections.Counter(train_labels_flat)

plt.figure(figsize=(8, 5))
plt.bar(counter.keys(), counter.values(), color='lightgreen')
plt.xlabel("Class Label")
plt.ylabel("Number of Images")
plt.title("Number of Training Images per Class (CIFAR-10)")
plt.xticks(range(10))
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()


from keras.applications.vgg16 import preprocess_input
def preprocess(image, label):
    image = tf.image.resize(image, (224, 224))  # Resize
    image = preprocess_input(image)  # Normalize using VGG16 preprocessing
    return image, label

# Convert to TensorFlow Dataset
train_ds = tf.data.Dataset.from_tensor_slices((x_train, y_train_onehot)).map(preprocess).batch(32)
test_ds = tf.data.Dataset.from_tensor_slices((x_test, y_test_onehot)).map(preprocess).batch(32)

model=models.Sequential()
model.add(conv_base)
model.add(layers.Flatten())
model.add(layers.Dense(256,activation='relu'))
model.add(layers.Dense(10,activation='softmax'))
model.summary()

from tensorflow.keras.optimizers import Adam
model.compile(optimizer=Adam(learning_rate=0.0001), loss='categorical_crossentropy', metrics=['accuracy'])


model.fit(train_ds, epochs=5, validation_data=test_ds)

# Evaluate Model
test_loss, test_acc = model.evaluate(test_ds)
print(f"Test Accuracy: {test_acc:.4f}")


from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
y_pred = model.predict(test_ds)
y_pred_classes = np.argmax(y_pred, axis=1)  # Convert from one-hot to class labels
y_true_classes = np.argmax(y_test_onehot, axis=1)  # Convert from one-hot to class labels

# Compute Confusion Matrix
conf_matrix = confusion_matrix(y_true_classes, y_pred_classes)

# Plot Confusion Matrix
plt.figure(figsize=(10, 7))
sns.heatmap(conf_matrix, annot=True, fmt="d", cmap="Blues", xticklabels=range(10), yticklabels=range(10))
plt.xlabel("Predicted Label")
plt.ylabel("True Label")
plt.title("Confusion Matrix for CIFAR-10")
plt.show()

