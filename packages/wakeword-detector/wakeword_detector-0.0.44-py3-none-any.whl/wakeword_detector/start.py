import subprocess
from .record_audio import record_samples
import signal

def main():
    try:
        print("\n🌐 Launching Wakeword Web UI at http://localhost:5000")
        print("👉 You can use the web interface, or press Enter to run the CLI setup wizard.\n")

        subprocess.Popen(["python", "-m", "wakeword_detector.dev_ui"])
        input("Press Enter to continue with CLI setup, or Ctrl+C to cancel...\n")

        print("\n👉 Step 1: Record wakeword samples")
        wake_count = 3
        record_samples(label="wakeword", count=wake_count, playback=True)

        print("\n👉 Step 2: Record negative/background samples")
        neg_count = 3
        record_samples(label="not-wakeword", count=neg_count, playback=False)

        print("\n✅ Recording complete!")
        print("\n✨ Next step: extract features and train your model:")
        print("   wakeword-detector extract")
        print("   wakeword-detector train")

    except KeyboardInterrupt:
        print("\n⛔ Cancelled by user.")
        exit(0)
