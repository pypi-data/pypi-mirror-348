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