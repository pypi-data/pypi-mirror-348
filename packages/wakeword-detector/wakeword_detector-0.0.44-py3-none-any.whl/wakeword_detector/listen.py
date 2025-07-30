import pyaudio
import numpy as np
import tensorflow as tf
import librosa
import os
import time
import sounddevice as sd
import wave

# Load the model
model = tf.keras.models.load_model("wakeword_model.pth")
threshold = 0.9  # High threshold for detecting wakeword

# Audio settings
rate = 16000
chunk = 1024
p = pyaudio.PyAudio()

# Function to record a false positive sample
def record_false_positive(filename="false_positive.wav", duration=3, fs=16000):
    print(f"Recording false positive sample: {filename}... Speak now!")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    print("Recording complete!")

    # Ensure output directory exists
    os.makedirs(os.path.dirname(filename) or ".", exist_ok=True)

    # Save to WAV
    with wave.open(filename, 'wb') as wavefile:
        wavefile.setnchannels(1)
        wavefile.setsampwidth(2)
        wavefile.setframerate(fs)
        wavefile.writeframes(recording.tobytes())

    print(f"💾 Saved: {filename}")
    return filename

def listen_for_wakeword():
    print("Listening for the wakeword...")

    # Open the audio stream for real-time detection
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=rate, input=True, frames_per_buffer=chunk)

    while True:
        audio_data = np.frombuffer(stream.read(chunk), dtype=np.int16)
        mfcc = librosa.feature.mfcc(y=audio_data.astype(float), sr=rate, n_mfcc=13)
        mfcc = np.expand_dims(mfcc, axis=0)

        # Model prediction
        prediction = model.predict(mfcc)[0][0]

        if prediction > threshold:
            print(f"✅ Wakeword detected! Probability: {prediction * 100:.2f}%")
        else:
            # If prediction is low, ask the user if it's a false positive
            print(f"⚠️ False positive detected! Probability: {prediction * 100:.2f}%")
            feedback = input("Is this a false positive? (y/n): ").strip().lower()

            if feedback == 'y':
                print("📝 Let's record the false positive...")
                filename = os.path.join(os.path.expanduser("~/wakeword_project/data/not-wakeword/"), "false_positive.wav")
                record_false_positive(filename)

                print("🔁 Retraining model with new data...")
                from wakeword_detector.train import train_wakeword_model
                train_wakeword_model()

        time.sleep(0.5)  # Wait before checking again

if __name__ == "__main__":
    listen_for_wakeword()
