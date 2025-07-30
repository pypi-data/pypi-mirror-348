import os
import numpy as np
import pyaudio
import librosa

# Conditional imports
import torch
import torch.nn as nn
import tensorflow as tf


class TorchWakewordModel(nn.Module):
    def __init__(self):
        super(TorchWakewordModel, self).__init__()
        self.fc1 = nn.Linear(13, 32)
        self.fc2 = nn.Linear(32, 16)
        self.fc3 = nn.Linear(16, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.sigmoid(self.fc3(x))
        return x


class WakewordDetector:
    def __init__(self, model_path="wakeword_model.h5", threshold=0.8):
        """Loads either a .h5 (TF) or .pth (Torch) wakeword model."""
        self.threshold = threshold
        self.rate = 16000
        self.chunk = 1024
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16, channels=1, rate=self.rate,
                                  input=True, frames_per_buffer=self.chunk)

        ext = os.path.splitext(model_path)[-1]

        if ext == ".h5":
            self.backend = "tf"
            self.model = tf.keras.models.load_model(model_path)
        elif ext == ".pth":
            self.backend = "torch"
            self.model = TorchWakewordModel()
            self.model.load_state_dict(torch.load(model_path, map_location="cpu"))
            self.model.eval()
        else:
            raise ValueError(f"Unsupported model format: {ext}")

    def detect(self):
        """Processes audio input and returns wakeword detection probability."""
        audio_data = np.frombuffer(self.stream.read(self.chunk), dtype=np.int16)
        mfcc = librosa.feature.mfcc(y=audio_data.astype(float), sr=self.rate, n_mfcc=13)

        if self.backend == "tf":
            mfcc_input = np.expand_dims(mfcc, axis=0)
            prediction = self.model.predict(mfcc_input)[0][0]

        elif self.backend == "torch":
            mfcc_input = np.mean(mfcc.T, axis=0)
            mfcc_tensor = torch.tensor(mfcc_input, dtype=torch.float32).unsqueeze(0)
            prediction = self.model(mfcc_tensor).item()

        return prediction > self.threshold, prediction

    def close(self):
        """Closes the audio stream."""
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
