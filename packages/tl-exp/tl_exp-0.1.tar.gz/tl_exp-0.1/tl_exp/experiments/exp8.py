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


