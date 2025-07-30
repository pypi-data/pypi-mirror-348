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


