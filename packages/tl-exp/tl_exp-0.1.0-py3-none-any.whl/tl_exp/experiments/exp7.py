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

