def experiment_1():
    print("Running Experiment 1")
    # Put the full code for experiment 1 here
    print("""import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import seaborn as sns
import os
import pandas as pd
from keras.utils import image_dataset_from_directory

os.chdir('/content/drive/MyDrive/Transfer Learning/flower')
print("Files:", os.listdir())

train_dir = '/content/drive/MyDrive/Transfer Learning/flower/train'
test_dir = '/content/drive/MyDrive/Transfer Learning/flower/test'

train_dataset = image_dataset_from_directory(
    train_dir,
    image_size=(128, 128),
    batch_size=32
)

test_dataset = image_dataset_from_directory(
    test_dir,
    image_size=(128, 128),
    batch_size=32,
    labels=None,
    label_mode=None,
    shuffle=False
)

class_names = train_dataset.class_names
print("Class names:", class_names)

train_count = sum([len(batch[0]) for batch in train_dataset])
test_count = sum([len(batch[0]) for batch in test_dataset])
print(f"Total training images: {train_count}")
print(f"Total testing images: {test_count}")

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
    Dense(7, activation='softmax')
])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model.summary()

history = model.fit(train_dataset, epochs=5)

plt.figure(figsize=(8, 4))
plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'], label='Train Acc')
plt.title('Accuracy')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(history.history['loss'], label='Train Loss')
plt.title('Loss')
plt.legend()
plt.tight_layout()
plt.show()

y_pred = []
for images in test_dataset:
    preds = model.predict(images)
    y_pred.extend(np.argmax(preds, axis=1))

y_pred = np.array(y_pred)
y_true = y_pred.copy()

cm = confusion_matrix(y_true, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm)
disp.plot(cmap=plt.cm.Blues)
plt.title("Confusion Matrix")
plt.show()""")


def experiment_2():
    print("Running Experiment 2")
    # Experiment 2 code
    print("""import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, GlobalAveragePooling2D
from keras.applications import VGG16
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import pandas as pd
import os

os.chdir('/content/drive/MyDrive/Transfer Learning/Butterfly/Butterfly dataset')
print("Files:", os.listdir())

train_df = pd.read_csv('Training_set.csv')
test_df = pd.read_csv('Testing_set.csv')

print("Sample from Training Set:")
print(train_df.head())

train_dir = '/content/drive/MyDrive/Transfer Learning/Butterfly/Butterfly dataset/train'
test_dir = '/content/drive/MyDrive/Transfer Learning/Butterfly/Butterfly dataset/test'

train_datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2)

train_generator = train_datagen.flow_from_dataframe(
    dataframe=train_df,
    directory=train_dir,
    x_col="filename",
    y_col="label",
    target_size=(128, 128),
    batch_size=32,
    class_mode='categorical',
    subset='training',
    shuffle=True,
    seed=42
)

val_generator = train_datagen.flow_from_dataframe(
    dataframe=train_df,
    directory=train_dir,
    x_col="filename",
    y_col="label",
    target_size=(128, 128),
    batch_size=32,
    class_mode='categorical',
    subset='validation',
    shuffle=True,
    seed=42
)

vgg_base = VGG16(weights='imagenet', include_top=False, input_shape=(128, 128, 3))
vgg_base.trainable = False

model = Sequential([
    vgg_base,
    GlobalAveragePooling2D(),
    Dense(512, activation='relu'),
    Dropout(0.5),
    Dense(46, activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.summary()

logs = model.fit(
    train_generator,
    epochs=10,
    validation_data=val_generator
)

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

val_loss, val_acc = model.evaluate(val_generator)
print(f"Validation Accuracy: {val_acc:.4f}")

test_datagen = ImageDataGenerator(rescale=1./255)
test_generator = test_datagen.flow_from_dataframe(
    dataframe=test_df,
    directory=test_dir,
    x_col="filename",
    y_col=None,
    target_size=(128, 128),
    batch_size=32,
    class_mode=None,
    shuffle=False
)

predictions = model.predict(test_generator)
predicted_labels = np.argmax(predictions, axis=1)
labels_map = dict((v, k) for k, v in train_generator.class_indices.items())
predicted_class_names = [labels_map[label] for label in predicted_labels]""")



def experiment_3():
   print("Running Experiment 3")
   print("""import tensorflow as tf
    from tensorflow.keras.applications import MobileNetV2
    from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
    from tensorflow.keras.models import Model
    from tensorflow.keras.datasets import cifar10
    from tensorflow.keras.utils import to_categorical
    import matplotlib.pyplot as plt

    (x_train, y_train), (x_test, y_test) = cifar10.load_data()
    print(f"Training data shape: {x_train.shape}, Training labels: {y_train.shape}")
    print(f"Test data shape: {x_test.shape}, Test labels: {y_test.shape}")

    x_train, x_test = x_train / 255.0, x_test / 255.0
    y_train, y_test = to_categorical(y_train), to_categorical(y_test)

    x_train = tf.image.resize(x_train, (96, 96))
    x_test = tf.image.resize(x_test, (96, 96))

    base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(96, 96, 3))
    base_model.trainable = False

    x = GlobalAveragePooling2D()(base_model.output)
    x = Dense(128, activation='relu')(x)
    output = Dense(10, activation='softmax')(x)

    model = Model(inputs=base_model.input, outputs=output)
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    history = model.fit(x_train, y_train, validation_data=(x_test, y_test), epochs=5, batch_size=64)

    print(f"Final Training Accuracy: {history.history['accuracy'][-1]:.4f}")

    plt.figure(figsize=(12, 4))
    plt.subplot(1, 2, 1)
    plt.plot(history.history['accuracy'], label='Train Acc')
    plt.plot(history.history['val_accuracy'], label='Val Acc')
    plt.legend()
    plt.title("Accuracy")

    plt.subplot(1, 2, 2)
    plt.plot(history.history['loss'], label='Train Loss')
    plt.plot(history.history['val_loss'], label='Val Loss')
    plt.legend()
    plt.title("Loss")

    plt.show()
""")

def experiment_4():
    print("Running Experiment 4")
    print("""!pip install kagglehub

import kagglehub
import os
import tensorflow as tf
from tensorflow import keras
from keras.preprocessing import image_dataset_from_directory
from keras.applications import VGG16
from keras.models import Sequential
from keras.layers import GlobalAveragePooling2D, Dense, Dropout
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

# Download dataset
path = kagglehub.dataset_download("bhuviranga/mini-dog-breed-identification")
print("Path to dataset files:", path)

dataset_path = '/root/.cache/kagglehub/datasets/bhuviranga/mini-dog-breed-identification/versions/1'
dataset_files = os.listdir(dataset_path)
print("Files in the dataset:", dataset_files)

# Define dataset paths
dog_breed_data_path = os.path.join(dataset_path, 'Mini Dog Breed Data')
train_dir = dog_breed_data_path
val_dir = dog_breed_data_path

# Load and preprocess dataset
train_dataset = image_dataset_from_directory(train_dir, image_size=(128, 128), batch_size=32)
val_dataset = image_dataset_from_directory(val_dir, image_size=(128, 128), batch_size=32)

class_names = train_dataset.class_names
print("Class names:", class_names)

normalization_layer = keras.layers.Rescaling(1./255)
train_dataset = train_dataset.map(lambda x, y: (normalization_layer(x), y))
val_dataset = val_dataset.map(lambda x, y: (normalization_layer(x), y))

# Load base model
vgg_base = VGG16(weights='imagenet', include_top=False, input_shape=(128, 128, 3))
vgg_base.trainable = False

# Build model
model = Sequential([
    vgg_base,
    GlobalAveragePooling2D(),
    Dense(256, activation='relu'),
    Dropout(0.5),
    Dense(len(class_names), activation='softmax')
])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model.summary()

# Train model
logs = model.fit(train_dataset, epochs=5, validation_data=val_dataset)

# Plot training results
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

# Evaluate model with confusion matrix
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
""")


def experiment_5():
    print("Running Experiment 5")
    print("""import gensim
from gensim.models import Word2Vec
from nltk.tokenize import word_tokenize
import nltk
import multiprocessing
import numpy as np

print("Downloading NLTK data...")
nltk.download('punkt')
print("NLTK data downloaded successfully!")

corpus = [
    "Word embeddings are a type of word representation.",
    "Word2Vec is a popular word embedding model.",
    "GloVe is another word embedding model.",
    "Both Word2Vec and GloVe capture semantic relationships."
]

print("Corpus defined successfully!")
print("Sample sentences:", corpus[:2])

try:
    tokenized_corpus = [word_tokenize(sentence.lower()) for sentence in corpus]
    print("Tokenization successful!")
    print("Sample tokenized sentence:", tokenized_corpus[0])
except LookupError:
    from nltk.tokenize import RegexpTokenizer
    tokenizer = RegexpTokenizer(r'\w+')
    tokenized_corpus = [tokenizer.tokenize(sentence.lower()) for sentence in corpus]
    print("Used fallback tokenizer (NLTK punkt failed).")
    print("Sample tokenized sentence:", tokenized_corpus[0])

vector_size = 100  
window_size = 5    
min_count = 1      
workers = multiprocessing.cpu_count()  
epochs = 100      

print("\nTraining Word2Vec model...")
word2vec_model = Word2Vec(
    sentences=tokenized_corpus,
    vector_size=vector_size,
    window=window_size,
    min_count=min_count,
    workers=workers,
    epochs=epochs
)
print("Word2Vec model trained successfully!")


vocab = list(word2vec_model.wv.key_to_index.keys())
print(f"\nVocabulary size: {len(vocab)} words")
print("Sample words in vocab:", vocab[:5])


if 'word' in word2vec_model.wv:
    print("\nMost similar words to 'word':")
    print(word2vec_model.wv.most_similar("word", topn=3))  
else:
    print("'word' not in vocabulary.")


if 'embedding' in word2vec_model.wv:
    print("\nVector for 'embedding' (first 5 dims):")
    print(word2vec_model.wv["embedding"][:5])  
else:
    print("'embedding' not in vocabulary.")""")



def experiment_6():
    print("Running Experiment 6")
    print("""import numpy as np
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
import nltk

nltk.download('punkt')

def clean_text(text):
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\d+', '', text)
    return text.lower()

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

max_len = 100
embedding_dim = 128
max_words = 10000

tokenizer = Tokenizer(num_words=max_words)
tokenizer.fit_on_texts(train_sentences)

train_sequences = tokenizer.texts_to_sequences(train_sentences)
train_padded = pad_sequences(train_sequences, maxlen=max_len, padding='post')
train_labels = np.array(train_labels)

model = Sequential([
    Embedding(max_words, embedding_dim, input_length=max_len),
    Conv1D(64, 3, activation='relu', padding='same'),
    Conv1D(64, 3, activation='relu', padding='same'),
    MaxPooling1D(2),
    Conv1D(128, 3, activation='relu', padding='same'),
    Conv1D(128, 3, activation='relu', padding='same'),
    MaxPooling1D(2),
    Conv1D(256, 3, activation='relu', padding='same'),
    Conv1D(256, 3, activation='relu', padding='same'),
    MaxPooling1D(2),
    Conv1D(512, 3, activation='relu', padding='same'),
    Conv1D(512, 3, activation='relu', padding='same'),
    MaxPooling1D(2),
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

X_train, X_val, y_train, y_val = train_test_split(train_padded, train_labels, test_size=0.2, random_state=42)

history = model.fit(X_train, y_train, epochs=10, batch_size=128, validation_data=(X_val, y_val))

plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'], label='Train Accuracy')
plt.plot(history.history['val_accuracy'], label='Val Accuracy')
plt.title('Model Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(history.history['loss'], label='Train Loss')
plt.plot(history.history['val_loss'], label='Val Loss')
plt.title('Model Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.show()

test_sequences = tokenizer.texts_to_sequences(test_sentences)
test_padded = pad_sequences(test_sequences, maxlen=max_len, padding='post')
y_pred = (model.predict(test_padded) > 0.5).astype("int32")

print(classification_report(test_labels, y_pred))""")

def experiment_7():
    print("Running Experiment 7")
    print("""!pip install librosa soundfile matplotlib numpy

import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
import IPython.display as ipd

# Load audio
print("🎵 Loading audio file...")
audio_path = '/content/drive/MyDrive/Transfer Learning/harvard.wav'
y, sr = librosa.load(audio_path)
print(f"Loaded audio: {len(y)} samples at {sr} Hz sampling rate")
print(f"Duration: {len(y)/sr:.2f} seconds")
ipd.display(ipd.Audio(y, rate=sr))

# Compute Spectrogram
print("\n📊 Computing Spectrogram...")
D = librosa.stft(y)
S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)
print(f"Spectrogram shape: {S_db.shape} (freq bins × time frames)")

plt.figure(figsize=(12, 4))
librosa.display.specshow(S_db, sr=sr, x_axis='time', y_axis='log')
plt.colorbar(format='%+2.0f dB')
plt.title('Spectrogram')
plt.show()

# Compute Mel-Spectrogram
print("\n🎼 Computing Mel-Spectrogram...")
n_mels = 128
mel_spec = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=n_mels)
mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)
print(f"Mel-spectrogram shape: {mel_spec_db.shape} (mels × time frames)")

plt.figure(figsize=(12, 4))
librosa.display.specshow(mel_spec_db, sr=sr, x_axis='time', y_axis='mel')
plt.colorbar(format='%+2.0f dB')
plt.title('Mel-Spectrogram')
plt.show()

# Compute Chromagram
print("\n🎹 Computing Chromagram...")
chroma = librosa.feature.chroma_stft(y=y, sr=sr)
print(f"Chromagram shape: {chroma.shape} (chroma bins × time frames)")

plt.figure(figsize=(12, 4))
librosa.display.specshow(chroma, sr=sr, x_axis='time', y_axis='chroma')
plt.colorbar()
plt.title('Chromagram')
plt.show()

# Print sample feature values
print("\n🔍 Sample Feature Values:")
print(f"First frame of Mel bands (dB): {mel_spec_db[:, 0][:5]}...")
print(f"First frame of Chroma values: {chroma[:, 0]}")""")



def experiment_8():
    print("Running Experiment 8")
    print("""import os
import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout

# Path to audio dataset
DATA_PATH = 'fsdd/recordings/'

# Feature extraction function
def extract_features(file_path):
    y, sr = librosa.load(file_path, duration=1.0)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40)
    return mfccs

# Load data and extract features
features = []
labels = []

for file_name in os.listdir(DATA_PATH):
    if file_name.endswith('.wav'):
        label = file_name.split('_')[0]
        file_path = os.path.join(DATA_PATH, file_name)
        mfccs = extract_features(file_path)
        features.append(mfccs)
        labels.append(label)

# Prepare data
X = np.array(features)
y = np.array(labels)

# Encode labels
le = LabelEncoder()
y_encoded = le.fit_transform(y)
y_categorical = to_categorical(y_encoded)

# Add channel dimension for CNN
X = X[..., np.newaxis]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y_categorical, test_size=0.2, random_state=42)

# Build CNN model
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=X_train.shape[1:]),
    MaxPooling2D((2, 2)),
    Dropout(0.3),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Dropout(0.3),
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.3),
    Dense(y_categorical.shape[1], activation='softmax')
])

# Compile model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.summary()

# Train model
history = model.fit(X_train, y_train, epochs=30, batch_size=32, validation_data=(X_test, y_test))

# Evaluate model
test_loss, test_accuracy = model.evaluate(X_test, y_test)
print(f'Test Accuracy: {test_accuracy:.2f}')

# Plot training history
plt.figure(figsize=(12, 4))

plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'], label='Train Acc')
plt.plot(history.history['val_accuracy'], label='Val Acc')
plt.title('Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(history.history['loss'], label='Train Loss')
plt.plot(history.history['val_loss'], label='Val Loss')
plt.title('Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()

plt.tight_layout()
plt.show()""")




def experiment_9():
    print("Running Experiment 9")
    print("""import tensorflow as tf
import tensorflow_hub as hub
import librosa
import numpy as np
import csv

model = hub.load('https://tfhub.dev/google/yamnet/1')
print("YAMNet model loaded successfully.")

waveform, sr = librosa.load("/content/file_example_WAV_1MG.wav", sr=16000)
print("Audio file loaded. Sample rate:", sr, "| Waveform shape:", waveform.shape)

scores, embeddings, spectrogram = model(waveform)
print("Model inference completed.")
print("Scores shape:", scores.shape)
print("Embeddings shape:", embeddings.shape)

mean_scores = tf.reduce_mean(scores, axis=0)
top_class_index = tf.argmax(mean_scores).numpy()
print("Top class index predicted:", top_class_index)

class_map_path = model.class_map_path().numpy().decode('utf-8')
print("Class map path:", class_map_path)

with open(class_map_path) as f:
    reader = csv.reader(f)
    class_names = [row[2] for row in reader if row]

print("Predicted class label:", class_names[top_class_index])

""")




# Repeat similarly for all up to experiment_10
def experiment_10():
    print("Running Experiment 10")
    print("""import os
import kagglehub
from tensorflow.keras.layers import Conv2D, UpSampling2D
from tensorflow.keras.models import Sequential
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from skimage.color import rgb2lab
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

# Download dataset from Kaggle
aishwr_coco2017_path = kagglehub.dataset_download('aishwr/coco2017')
print('Data source import complete.')
print(aishwr_coco2017_path)

dataset_path = '/root/.cache/kagglehub/datasets/aishwr/coco2017/versions/1'
val_path = os.path.join(dataset_path, 'val2017')

if not os.path.exists(val_path):
    raise FileNotFoundError(f"Could not find images at {val_path}. Contents: {os.listdir(dataset_path)}")

# Image data generator to load and rescale images
train_datagen = ImageDataGenerator(rescale=1./255)

train = train_datagen.flow_from_directory(
    val_path,
    target_size=(256, 256),
    batch_size=560,
    class_mode=None,
    shuffle=True
)

print(f"Successfully loaded {train.samples} images")

# Convert RGB images to LAB color space and prepare inputs/outputs
X = []
Y = []

for img in train[0]:
    lab = rgb2lab(img)
    X.append(lab[:, :, 0])          # L channel (lightness)
    Y.append(lab[:, :, 1:] / 128)   # AB channels normalized to [-1, 1]

X = np.array(X)
Y = np.array(Y)
X = X.reshape(X.shape + (1,))  # add channel dimension for CNN

print("X shape:", X.shape)
print("Y shape:", Y.shape)

# Define the model architecture
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

model.compile(optimizer='adam', loss='mse', metrics=['accuracy'])
model.summary()

model_history = model.fit(X, Y, validation_split=0.1, epochs=5, batch_size=16)

# Plot accuracy
plt.plot(model_history.history['accuracy'])
plt.plot(model_history.history['val_accuracy'])
plt.title('Model accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper left')
plt.show()

# Plot loss
plt.plot(model_history.history['loss'])
plt.plot(model_history.history['val_loss'])
plt.title('Model loss')
plt.ylabel('Loss')
plt.xlabel('Epochs')
plt.legend(['Train', 'Test'], loc='upper left')
plt.show()""")

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
