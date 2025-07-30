def experiment_1():
    print("Running Experiment 1")
    # Put the full code for experiment 1 here
    def run():
    import numpy as np
    import matplotlib.pyplot as plt
    import tensorflow as tf
    from tensorflow import keras
    from keras.models import Sequential
    from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
    from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
    import seaborn as sns
    import os
    import pandas as pd

    os.chdir('/content/drive/MyDrive/Cars Dataset')

    train_dir = '/content/drive/MyDrive/Cars Dataset/train'
    test_dir = '/content/drive/MyDrive/Cars Dataset/test'

    from keras.utils import image_dataset_from_directory

    train_dataset = image_dataset_from_directory(train_dir, image_size=(128, 128), batch_size=32, shuffle=True)
    test_dataset = image_dataset_from_directory(test_dir, image_size=(128, 128), batch_size=32, shuffle=False)

    class_names = train_dataset.class_names
    print("\nClass names:", class_names)

    train_count = sum([len(batch[0]) for batch in train_dataset])
    test_count = sum([len(batch[0]) for batch in test_dataset])
    print(f"\nTotal training images: {train_count}")
    print(f"Total testing images: {test_count}")

    class_counts = [0] * len(class_names)
    for _, labels in train_dataset.unbatch():
        class_counts[int(labels.numpy())] += 1

    df = pd.DataFrame({'Car Class': class_names, 'Count': class_counts})
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Car Class', y='Count', data=df, palette='pastel')
    plt.title("Training Images per Car Class")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(10, 10))
    for images, labels in train_dataset.take(1):
        for i in range(9):
            ax = plt.subplot(3, 3, i + 1)
            plt.imshow(images[i].numpy().astype("uint8"))
            plt.title(f"Label: {class_names[labels[i]]}")
            plt.axis("off")

    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=(128, 128, 3)),
        MaxPooling2D(2, 2),
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D(2, 2),
        Conv2D(128, (3, 3), activation='relu'),
        MaxPooling2D(2, 2),
        Flatten(),
        Dense(128, activation='relu'),
        Dropout(0.5),
        Dense(len(class_names), activation='softmax')
    ])
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    model.summary()

    logs = model.fit(train_dataset, epochs=10, validation_data=test_dataset)

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

    y_true = np.concatenate([labels.numpy() for _, labels in test_dataset])
    y_pred = []

    for images, _ in test_dataset:
        preds = model.predict(images)
        y_pred.extend(np.argmax(preds, axis=1))

    y_pred = np.array(y_pred)

    cm = confusion_matrix(y_true, y_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=class_names)

    plt.figure(figsize=(10, 8))
    disp.plot(cmap=plt.cm.Blues, xticks_rotation=45)
    plt.title("Confusion Matrix")
    plt.tight_layout()
    plt.show()

    test_counts = [0] * len(class_names)
    for _, labels in test_dataset.unbatch():
        test_counts[int(labels.numpy())] += 1

    for class_name, count in zip(class_names, test_counts):
        print(f"{class_name}: {count} test images")

    train_y_true = []
    train_y_pred = []

    for images, labels in train_dataset:
        preds = model.predict(images)
        train_y_pred.extend(np.argmax(preds, axis=1))
        train_y_true.extend(labels.numpy())

    cm_train = confusion_matrix(train_y_true, train_y_pred)
    disp_train = ConfusionMatrixDisplay(confusion_matrix=cm_train, display_labels=class_names)

    plt.figure(figsize=(10, 8))
    disp_train.plot(cmap=plt.cm.Oranges, xticks_rotation=45)
    plt.title("Confusion Matrix - Training Data")
    plt.tight_layout()
    plt.show()


def experiment_2():
    print("Running Experiment 2")
    # Experiment 2 code
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



def experiment_3():
    print("Running Experiment 3")
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

def experiment_4():
    print("Running Experiment 4")
    !pip install kagglehub


import kagglehub
path = kagglehub.dataset_download("bhuviranga/mini-dog-breed-identification")
print("Path to dataset files:", path)

import os
dataset_path = '/root/.cache/kagglehub/datasets/bhuviranga/mini-dog-breed-identification/versions/1'
dataset_files = os.listdir(dataset_path)
print("Files in the dataset:", dataset_files)


dog_breed_data_path = os.path.join(dataset_path, 'Mini Dog Breed Data')
dog_breed_data_files = os.listdir(dog_breed_data_path)
print("Files in the 'Mini Dog Breed Data' directory:")
for file in dog_breed_data_files:
    print(file)


import tensorflow as tf
from tensorflow import keras
from keras.preprocessing import image_dataset_from_directory
import os
from keras.applications import VGG16
from keras.models import Sequential
from keras.layers import GlobalAveragePooling2D, Dense, Dropout

dog_breed_data_path = os.path.join(dataset_path, 'Mini Dog Breed Data')
train_dir = dog_breed_data_path
val_dir = dog_breed_data_path
train_dataset = image_dataset_from_directory(train_dir, image_size=(128, 128), batch_size=32)
val_dataset = image_dataset_from_directory(val_dir, image_size=(128, 128), batch_size=32)
class_names = train_dataset.class_names
print("\nClass names:", class_names)

class_counts = [0] * len(class_names)
for _, labels in train_dataset.unbatch():
    class_counts[int(labels.numpy())] += 1

# Plot histogram of class distribution
import matplotlib.pyplot as plt
plt.figure(figsize=(10, 6))
plt.bar(class_names, class_counts, color='skyblue')
plt.xticks(rotation=45)
plt.xlabel("Dog Breed")
plt.ylabel("Number of Images")
plt.title("Number of Images per Dog Breed")
plt.tight_layout()
plt.show()

normalization_layer = keras.layers.Rescaling(1./255)
train_dataset = train_dataset.map(lambda x, y: (normalization_layer(x), y))
val_dataset = val_dataset.map(lambda x, y: (normalization_layer(x), y))

vgg_base = VGG16(weights='imagenet', include_top=False, input_shape=(128, 128, 3))
vgg_base.trainable = False
model = Sequential([
    vgg_base,
    GlobalAveragePooling2D(),
    Dense(256, activation='relu'),
    Dropout(0.5),
    Dense(len(class_names), activation='softmax')
])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model.summary()

logs = model.fit(train_dataset, epochs=5, validation_data=val_dataset)

# Plot accuracy and loss
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

import numpy as np
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt
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
plt.title("Confusion Matrix for Dog Breed Classification")
plt.show()


def experimrnt_5():
    print("Running Experiment 5")
    import gensim
from gensim.models import Word2Vec
from nltk.tokenize import word_tokenize
import nltk
import multiprocessing

print("⏳ Downloading NLTK data...")
nltk.download('punkt')
nltk.download('punkt_tab')
print("✅ NLTK data downloaded successfully!")

corpus = [
    "Word embeddings are a type of word representation.",
    "Word2Vec is a popular word embedding model.",
    "GloVe is another word embedding model.",
    "Both Word2Vec and GloVe capture semantic relationships."
]

print("📜 Corpus defined successfully!")
print("Sample sentences:", corpus[:2])

try:
    tokenized_corpus = [word_tokenize(sentence.lower()) for sentence in corpus]
    print("🔡 Tokenization successful!")
    print("Sample tokenized sentence:", tokenized_corpus[0])
except LookupError:
    from nltk.tokenize import RegexpTokenizer
    tokenizer = RegexpTokenizer(r'\w+')
    tokenized_corpus = [tokenizer.tokenize(sentence.lower()) for sentence in corpus]
    print("⚠️ Used fallback tokenizer (NLTK punkt failed).")
    print("Sample tokenized sentence:", tokenized_corpus[0])


vector_size = 100  # Dimension of word vectors
window_size = 5    # Context window size
min_count = 1      # Minimum word frequency
workers = multiprocessing.cpu_count()  # Use all CPU cores
epochs = 100       # Training iterations

print("⚙️ Word2Vec parameters set:")
print(f"- Vector size: {vector_size}")
print(f"- Window size: {window_size}")
print(f"- Min word count: {min_count}")
print(f"- Workers: {workers}")
print(f"- Epochs: {epochs}")

# Step 7: Check vocabulary and sample outputs
vocab = list(word2vec_model.wv.key_to_index.keys())
print(f" Vocabulary size: {len(vocab)} words")
print("Sample words in vocab:", vocab[:5])  # First 5 words

# Check if 'word' is in vocab
if 'word' in word2vec_model.wv:
    print("\n Most similar words to 'word':")
    print(word2vec_model.wv.most_similar("word", topn=3))  # Top 3 similar words
else:
    print("'word' not in vocabulary.")

# Get vector for 'embedding'
if 'embedding' in word2vec_model.wv:
    print("\n Vector for 'embedding' (first 5 dims):")
    print(word2vec_model.wv["embedding"][:5])  # Show first 5 dimensions
else:
    print("'embedding' not in vocabulary.")

## **GLOVE MODEL**

!wget http://nlp.stanford.edu/data/glove.6B.zip
!unzip glove.6B.zip

import numpy as np

def load_glove_embeddings(path):
    embeddings = {}
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            values = line.split()
            word = values[0]
            vector = np.asarray(values[1:], dtype='float32')
            embeddings[word] = vector
    return embeddings

glove_path = 'glove.6B.100d.txt'
glove_embeddings = load_glove_embeddings(glove_path)

print(f"Loaded {len(glove_embeddings)} word vectors")
print("Vector for 'king':", glove_embeddings['king'][:5])  # Show first 5 dimensions
print("Most similar to 'paris':", sorted(
    [(word, np.dot(glove_embeddings['paris'], glove_embeddings[word]))
     for word in ['france', 'london', 'berlin']],
    key=lambda x: -x[1]
))



def experimrnt_6():
    print("Running Experiment 6")
    import numpy as np
import tensorflow as tf
import tensorflow_datasets as tfds
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, Conv1D, MaxPooling1D, Flatten, Dense, Dropout
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import re
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt

nltk.download('punkt')

def clean_text(text):
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\d+', '', text)
    text = text.lower()
    return text

def load_imdb_data():
    imdb, info = tfds.load('imdb_reviews', with_info=True, as_supervised=True)

    train_data = imdb['train']
    train_sentences, train_labels = [], []
    for sentence, label in tfds.as_numpy(train_data):
        train_sentences.append(clean_text(sentence.decode('utf-8')))
        train_labels.append(int(label))

    test_data = imdb['test']
    test_sentences, test_labels = [], []
    for sentence, label in tfds.as_numpy(test_data):
        test_sentences.append(clean_text(sentence.decode('utf-8')))
        test_labels.append(int(label))

    return train_sentences, train_labels, test_sentences, test_labels

train_sentences, train_labels, test_sentences, test_labels = load_imdb_data()

# Define parameters
max_len = 100
embedding_dim = 128
max_words = 10000

# Tokenizer
tokenizer = Tokenizer(num_words=max_words)
tokenizer.fit_on_texts(train_sentences)

# Prepare training data
train_sequences = tokenizer.texts_to_sequences(train_sentences)
train_padded = pad_sequences(train_sequences, maxlen=max_len, padding='post')
train_labels = np.array(train_labels)

model = Sequential([
    Embedding(max_words, embedding_dim, input_length=max_len),

    # Block 1
    Conv1D(64, 3, activation='relu', padding='same'),
    Conv1D(64, 3, activation='relu', padding='same'),
    MaxPooling1D(2),

    # Block 2
    Conv1D(128, 3, activation='relu', padding='same'),
    Conv1D(128, 3, activation='relu', padding='same'),
    MaxPooling1D(2),

    # Block 3
    Conv1D(256, 3, activation='relu', padding='same'),
    Conv1D(256, 3, activation='relu', padding='same'),
    MaxPooling1D(2),

    # Block 4
    Conv1D(512, 3, activation='relu', padding='same'),
    Conv1D(512, 3, activation='relu', padding='same'),
    MaxPooling1D(2),

    # Block 5
    Conv1D(512, 3, activation='relu', padding='same'),
    Conv1D(512, 3, activation='relu', padding='same'),
    MaxPooling1D(2),

    Flatten(),
    Dense(4096, activation='relu'),
    Dropout(0.5),
    Dense(4096, activation='relu'),
    Dropout(0.5),
    Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Split data
X_train, X_val, y_train, y_val = train_test_split(train_padded, train_labels, test_size=0.2, random_state=42)

# Train
history = model.fit(X_train, y_train, epochs=10, batch_size=128, validation_data=(X_val, y_val))

plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'], label='train accuracy')
plt.plot(history.history['val_accuracy'], label='val accuracy')
plt.title('Model Accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(history.history['loss'], label='train loss')
plt.plot(history.history['val_loss'], label='val loss')
plt.title('Model Loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend()
plt.show()

test_sequences = tokenizer.texts_to_sequences(test_sentences)
test_padded = pad_sequences(test_sequences, maxlen=max_len, padding='post')
y_pred = (model.predict(test_padded) > 0.5).astype("int32")
print(classification_report(test_labels, y_pred))

model.summary()

def experimrnt_7():
    print("Running Experiment 7")
    !pip install librosa soundfile matplotlib numpy

import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
import IPython.display as ipd

print("1️⃣ Loading audio file...")
audio_path = '/content/drive/MyDrive/Transfer Learning/harvard.wav'
y, sr = librosa.load(audio_path)
print(f"✅ Loaded audio: {len(y)} samples at {sr}Hz sampling rate")


print(f"Duration: {len(y)/sr:.2f} seconds")
ipd.display(ipd.Audio(y, rate=sr))

print("\nComputing Spectrogram")
D = librosa.stft(y)
S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)
print(f"Spectrogram shape: {S_db.shape} (freq bins × time frames)")

plt.figure(figsize=(12, 4))
librosa.display.specshow(S_db, sr=sr, x_axis='time', y_axis='log')
plt.colorbar(format='%+2.0f dB')
plt.title('Spectrogram')
plt.show()

print("\n Computing Mel-Spectrogram")
n_mels = 128
mel_spec = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=n_mels)
mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)
print(f"Mel-spectrogram shape: {mel_spec_db.shape} (mels × time frames)")

plt.figure(figsize=(12, 4))
librosa.display.specshow(mel_spec_db, sr=sr, x_axis='time', y_axis='mel')
plt.colorbar(format='%+2.0f dB')
plt.title('Mel-Spectrogram')
plt.show()

print("\nComputing Chromagram")
chroma = librosa.feature.chroma_stft(y=y, sr=sr)
print(f"Chromagram shape: {chroma.shape} (chroma bins × time frames)")

plt.figure(figsize=(12, 4))
librosa.display.specshow(chroma, sr=sr, x_axis='time', y_axis='chroma')
plt.colorbar()
plt.title('Chromagram')
plt.show()

print("Sample Feature Values:")
print(f"First frame of Mel bands (dB): {mel_spec_db[:, 0][:5]}...")
print(f"First frame of Chroma values: {chroma[:, 0]}")



def experimrnt_8():
    print("Running Experiment 8")
    !mkdir -p "/content/drive/MyDrive/Transfer Learning/Audio"


!unzip "/content/drive/MyDrive/Transfer Learning/Audio.zip" -d "/content/drive/MyDrive/Transfer Learning/Audio"

!pip install librosa matplotlib scikit-learn tensorflow

import os
import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout


import os
import librosa
import numpy as np

# Your data folder
base_path = "/content/drive/MyDrive/Transfer Learning/Audio/audio/audio"

# Two subfolders: "16000" and "44100"
subfolders = ['16000', '44100']

# Define some parameters
SAMPLE_RATE = 16000  # Choose a common sampling rate for all
DURATION = 3         # Seconds
SAMPLES_PER_TRACK = SAMPLE_RATE * DURATION

# Store features and labels
X = []
y = []

for folder in subfolders:
    folder_path = os.path.join(base_path, folder)
    print(f"Loading folder: {folder_path}")

    # Go through each file
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)

        # Only load audio files (.wav)
        if file_name.endswith('.wav'):
            try:
                y_audio, sr = librosa.load(file_path, sr=SAMPLE_RATE)

                # Cut or pad to the same length
                if len(y_audio) > SAMPLES_PER_TRACK:
                    y_audio = y_audio[:SAMPLES_PER_TRACK]
                else:
                    y_audio = np.pad(y_audio, (0, SAMPLES_PER_TRACK - len(y_audio)))

                # Feature extraction — Example: Mel Spectrogram
                mel_spectrogram = librosa.feature.melspectrogram(y=y_audio, sr=SAMPLE_RATE)
                mel_spectrogram_db = librosa.power_to_db(mel_spectrogram, ref=np.max)

                # Resize to fixed shape (optional but good for CNNs)
                mel_spectrogram_db = librosa.util.fix_length(mel_spectrogram_db, size=128, axis=1)

                # Save feature and label
                X.append(mel_spectrogram_db)
                y.append(folder)  # Label is the folder name ("16000" or "44100")

            except Exception as e:
                print(f"Failed to load {file_path}: {e}")

X = np.array(X)
y = np.array(y)

print("\nLoaded data:")
print("X shape:", X.shape)
print("y shape:", y.shape)
print("Labels:", np.unique(y))


import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.utils import to_categorical


# Encode string labels ('16000', '44100') into numbers (0,1)
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# One-hot encode the labels
y_categorical = to_categorical(y_encoded)


X_train, X_test, y_train, y_test = train_test_split(
    X, y_categorical, test_size=0.2, random_state=42, stratify=y_encoded)

# Add a channel dimension
X_train = X_train[..., np.newaxis]
X_test = X_test[..., np.newaxis]


model = Sequential([
    Conv2D(32, (3,3), activation='relu', input_shape=(128,128,1)),
    MaxPooling2D((2,2)),
    Conv2D(64, (3,3), activation='relu'),
    MaxPooling2D((2,2)),
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(2, activation='softmax')  # 2 classes: 16000 or 44100
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.summary()


history = model.fit(X_train, y_train, epochs=8, batch_size=32,
                    validation_data=(X_test, y_test))


model.save('audio_classifier_model.h5')

# Accuracy graph
import matplotlib.pyplot as plt
plt.plot(history.history['accuracy'], label='train acc')
plt.plot(history.history['val_accuracy'], label='val acc')
plt.legend()
plt.title('Accuracy')
plt.show()

# Loss graph
plt.plot(history.history['loss'], label='train loss')
plt.plot(history.history['val_loss'], label='val loss')
plt.legend()
plt.title('Loss')
plt.show()




def experimrnt_9():
    print("Running Experiment 9")
    import pandas as pd
metadata= pd.read_csv('/content/drive/MyDrive/archive-2/esc50.csv')
metadata.head(15)

#checking dataset
metadata['take'].value_counts()

from google.colab import drive
drive.mount('/content/drive')

#read a sample audio using librosa
import librosa
audio_file_path='/content/drive/MyDrive/archive-2/audio/audio/1-100032-A-0.wav'
librosa_audio_data,librosa_sample_rate=librosa.load(audio_file_path)

print(librosa_audio_data)

#plotting the librosa audio data
import matplotlib.pyplot as plt
plt.figure(figsize=(15, 5))   # Original audio with 1 channel
plt.plot(librosa_audio_data)

from scipy.io import wavfile as wav  #Performing the same process wid scipy
wave_sample_rate, wave_audio = wav.read(audio_file_path)

wave_audio

import matplotlib.pyplot as plt


plt.figure(figsize=(15, 5)) # Original audio with 2 channels
plt.plot(wave_audio)

# Importing necessary libraries againd

# Data preprocessing
import pandas as pd
import numpy as np
import os, librosa
from tqdm import tqdm
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Visualization
import IPython.display as ipd
import matplotlib.pyplot as plt
import seaborn as sns

# Model
from tensorflow import keras
from keras.utils import to_categorical
from keras import layers, Sequential
from keras.callbacks import EarlyStopping, ReduceLROnPlateau
from keras.layers import Conv2D, MaxPooling2D,BatchNormalization

# Metrics
from sklearn.metrics import confusion_matrix

# Suppressing warnings
from warnings import filterwarnings
filterwarnings('ignore')

mfccs = librosa.feature.mfcc(y=librosa_audio_data, sr=librosa_sample_rate, n_mfcc=40)
print(mfccs.shape)

mfccs

#for all the files we will be performing it in following manner
import pandas as pd
import os
import librosa

audio_dataset_path = '/content/drive/MyDrive/archive-2/audio/audio'
metadata =  pd.read_csv('/content/drive/MyDrive/archive-2/esc50.csv')
metadata.head()

# Computing Mel-frequency cepstral coefficients
def mfccExtract(file):
    # Loading audio file
    waveform, sampleRate = librosa.load(file_name)

    features = librosa.feature.mfcc(y = waveform, sr = sampleRate, n_mfcc = 50)
    return np.mean(features, axis = 1)


extractAll = []

import numpy as np
from tqdm import tqdm
# Iterating through each row
for index_num, row in tqdm(metadata.iterrows()):

    file_name = os.path.join(audio_dataset_path,  row['filename'])

    features = mfccExtract(file_name)
    extractAll.append([features, row['take']])

featuresDf = pd.DataFrame(extractAll, columns = ['Features', 'take'])
featuresDf.head()

### Split the dataset into independent and dependent dataset
X=np.array(featuresDf['Features'].tolist())
Y=np.array(featuresDf['take'].tolist())

X.shape

Y

### Label Encoding
###y=np.array(pd.get_dummies(y))
### Label Encoder
from tensorflow.keras.utils import to_categorical
from sklearn.preprocessing import LabelEncoder
labelencoder=LabelEncoder()
Y=to_categorical(labelencoder.fit_transform(Y))

Y

### Train Test Split
from sklearn.model_selection import train_test_split
X_train,X_test,Y_train,Y_test=train_test_split(X,Y,test_size=0.2,random_state=0)

X_train

X_train.shape

X_test.shape

Y_train.shape

### No of classes
num_labels=Y.shape[1]

### No of classes
num_labels=Y.shape[1]
# %%
model = Sequential([
    layers.Dense(1024, activation = 'relu', input_shape = (50,)), #above we have kept the value of features as 50
    layers.BatchNormalization(), #first layer

    layers.Dense(512, activation = 'relu'),
    layers.BatchNormalization(),

    layers.Dense(256, activation = 'relu'),
    layers.BatchNormalization(),

    layers.Dense(128, activation = 'relu'),
    layers.BatchNormalization(),

    layers.Dense(64, activation = 'relu'),
    layers.BatchNormalization(),

    layers.Dense(32, activation = 'relu'),
    layers.BatchNormalization(),

    layers.Dense(num_labels, activation = 'softmax') # Change to num_labels instead of 10
])
model.compile(loss='categorical_crossentropy',metrics=['accuracy'],optimizer='adam')
model.summary()

history = model.fit(X_train, Y_train, validation_data = (X_test, Y_test), epochs = 10)

test_accuracy=model.evaluate(X_test,Y_test,verbose=0)
print(test_accuracy[1])

historyDf = pd.DataFrame(history.history)

# Plotting training and validation loss
historyDf.loc[:, ['loss', 'val_loss']].plot()

# Plotting training and validation accuracy
historyDf.loc[:, ['accuracy', 'val_accuracy']].plot()

# Evaluating model
score = model.evaluate(X_test, Y_test)[1] * 100
print(f'Validation accuracy of model : {score:.2f}%')





# Repeat similarly for all up to experiment_10
def experiment_10():
    print("Running Experiment 10")
    import kagglehub
aishwr_coco2017_path = kagglehub.dataset_download('aishwr/coco2017')

print('Data source import complete.')


# For TensorFlow 2.x and Keras 2.x:
from tensorflow.keras.layers import Conv2D, UpSampling2D
from tensorflow.keras.models import Sequential
from tensorflow.keras.preprocessing.image import ImageDataGenerator, img_to_array, load_img

# The rest can stay the same:
from skimage.color import rgb2lab, lab2rgb
from skimage.transform import resize
from skimage.io import imsave
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from skimage import io

print(aishwr_coco2017_path)  # This shows the exact download path

dataset_path = '/root/.cache/kagglehub/datasets/aishwr/coco2017/versions/1'
val_path = os.path.join(dataset_path, 'val2017')

if not os.path.exists(val_path):
    raise FileNotFoundError(f"Could not find images at {val_path}. Contents: {os.listdir(dataset_path)}")


train_datagen = ImageDataGenerator(rescale=1./255)

train = train_datagen.flow_from_directory(
    val_path,
    target_size=(256, 256),
    batch_size=560,
    class_mode=None,  # Important for autoencoder tasks
    shuffle=True      # Recommended for training
)

print(f"Successfully loaded {train.samples} images")

#Convert from RGB to Lab

X =[]
Y =[]
for img in train[0]:
  try:
      lab = rgb2lab(img)
      X.append(lab[:,:,0])
      Y.append(lab[:,:,1:] / 128) #A and B values range from -127 to 128,
      #so we divide the values by 128 to restrict values to between -1 and 1.
  except:
     print('error')
X = np.array(X)
Y = np.array(Y)
X = X.reshape(X.shape+(1,)) #dimensions to be the same for X and Y
print(X.shape)
print(Y.shape)

#Encoder

model = Sequential()
model.add(Conv2D(64, (3, 3), activation='relu', padding='same', strides=2, input_shape=(256, 256, 1)))
model.add(Conv2D(128, (3, 3), activation='relu', padding='same'))
model.add(Conv2D(128, (3,3), activation='relu', padding='same', strides=2))
model.add(Conv2D(256, (3,3), activation='relu', padding='same'))
model.add(Conv2D(256, (3,3), activation='relu', padding='same', strides=2))
model.add(Conv2D(512, (3,3), activation='relu', padding='same'))
model.add(Conv2D(512, (3,3), activation='relu', padding='same'))
model.add(Conv2D(256, (3,3), activation='relu', padding='same'))


model.add(Conv2D(128, (3,3), activation='relu', padding='same'))
model.add(UpSampling2D((2, 2)))
model.add(Conv2D(64, (3,3), activation='relu', padding='same'))
model.add(UpSampling2D((2, 2)))
model.add(Conv2D(32, (3,3), activation='relu', padding='same'))
model.add(Conv2D(16, (3,3), activation='relu', padding='same'))
model.add(Conv2D(2, (3, 3), activation='tanh', padding='same'))
model.add(UpSampling2D((2, 2)))

model.compile(optimizer='adam', loss='mse' , metrics=['accuracy'])
model.summary()

model_history = model.fit(X,Y,validation_split=0.1, epochs=5, batch_size=16)

 # Plot training & validation accuracy values
plt.plot(model_history.history['accuracy'])
plt.plot(model_history.history['val_accuracy'])
plt.title('Model accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper left')
plt.show()

# Plot training & validation loss values
plt.plot(model_history.history['loss'])
plt.plot(model_history.history['val_loss'])
plt.title('Model loss')
plt.ylabel('Loss')
plt.xlabel('Epochs')
plt.legend(['Train', 'Test'], loc='upper left')
plt.show()

def tl_exp(exp_number):
    experiments = {
        1: experiment_1,
        2: experiment_2,
        3: experiment_3,
        4: experiment_4,
        5: experiment_5,
        6: experiment_6,
        7: experiment_7,
        8: experiment_8,
        9: experiment_9,
        10: experiment_10,
    }
    if exp_number in experiments:
        experiments[exp_number]()
    else:
        raise ValueError("Invalid experiment number. Choose between 1 and 10.")
