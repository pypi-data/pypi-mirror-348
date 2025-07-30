import sounddevice as sd
import numpy as np
import wave
import os
import argparse
from datetime import datetime

DEFAULT_DATA_PATH = os.path.expanduser("~/wakeword_project/data")

def record_sample(filename, fs=16000):
    """Record audio interactively and save as a WAV file."""
    print(f"🎙️ Press Enter to start recording...")
    input()
    print("🔴 Recording... Press Enter to stop (or Ctrl+C to cancel)")

    recording = []

    def callback(indata, frames, time, status):
        recording.append(indata.copy())

    try:
        stream = sd.InputStream(callback=callback, samplerate=fs, channels=1)
        stream.start()

        input()  # Wait for user to press Enter again
        stream.stop()
        stream.close()

        full_recording = np.concatenate(recording, axis=0)
        print("✅ Recording stopped.")

        os.makedirs(os.path.dirname(filename) or ".", exist_ok=True)

        with wave.open(filename, 'wb') as wavefile:
            wavefile.setnchannels(1)
            wavefile.setsampwidth(2)
            wavefile.setframerate(fs)
            wavefile.writeframes(full_recording.astype(np.int16).tobytes())

        print(f"💾 Saved: {filename}")
        return filename

    except KeyboardInterrupt:
        print("\n⛔ Recording cancelled by user.")
        try:
            stream.stop()
            stream.close()
        except:
            pass
        return None

def record_samples(label, count=1, playback=False):
    label_dir = os.path.join(DEFAULT_DATA_PATH, label)
    os.makedirs(label_dir, exist_ok=True)

    print(f"\n📁 Saving to: {label_dir}")
    print(f"🗣️ Recording {count} sample(s) of '{label}'...\n")

    for i in range(1, count + 1):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(label_dir, f"{label}_{timestamp}_{i:02}.wav")

        print(f"[{i}/{count}]")
        saved_path = record_sample(filename)

        if saved_path and playback:
            print("▶️ Playing back...")
            import soundfile as sf
            data, fs = sf.read(saved_path, dtype='int16')
            sd.play(data, fs)
            sd.wait()

def parse_record_args():
    parser = argparse.ArgumentParser(description="Record labeled audio samples.")
    parser.add_argument("--count", type=int, default=1, help="Number of samples to record")
    parser.add_argument("--playback", action="store_true", help="Play audio after recording")
    return parser.parse_args()

def record_wakeword_main():
    args = parse_record_args()
    record_samples(label="wakeword", count=args.count, playback=args.playback)

def record_negative_main():
    args = parse_record_args()
    record_samples(label="not-wakeword", count=args.count, playback=args.playback)
