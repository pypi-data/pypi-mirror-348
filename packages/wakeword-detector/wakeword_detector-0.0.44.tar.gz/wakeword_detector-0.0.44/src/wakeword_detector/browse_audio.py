import os
import sounddevice as sd
import soundfile as sf
import argparse
import shutil

DEFAULT_DATA_PATH = os.path.expanduser("~/wakeword_project/data")

def list_audio_files(category=None):
    files = []
    index = 1
    indexed_files = {}

    for subfolder in sorted(os.listdir(DEFAULT_DATA_PATH)):
        if category and subfolder != category:
            continue

        full_path = os.path.join(DEFAULT_DATA_PATH, subfolder)
        if not os.path.isdir(full_path):
            continue

        print(f"\n📁 Category: {subfolder}")
        for fname in sorted(os.listdir(full_path)):
            if fname.endswith(".wav"):
                path = os.path.join(full_path, fname)
                print(f"[{index}] {fname}")
                indexed_files[str(index)] = path
                index += 1

    return indexed_files

def play_audio(path):
    print(f"\n🔊 Playing: {os.path.basename(path)}")
    data, fs = sf.read(path, dtype='int16')
    sd.play(data, fs)
    sd.wait()

def browse(category=None, delete=False, export_path=None):
    indexed = list_audio_files(category)

    if not indexed:
        print("\n⚠️ No audio files found.")
        return

    while True:
        choice = input("\n▶️ Enter number to play, 'q' to quit: ").strip()

        if choice.lower() == 'q':
            break
        elif choice in indexed:
            path = indexed[choice]
            play_audio(path)

            if delete:
                confirm = input("❌ Delete this file? [y/N]: ").strip().lower()
                if confirm == 'y':
                    os.remove(path)
                    print("🗑️ Deleted.")
                    indexed.pop(choice)

            if export_path:
                os.makedirs(export_path, exist_ok=True)
                shutil.copy(path, export_path)
                print(f"📤 Exported to: {export_path}")
        else:
            print("❌ Invalid choice.")

def parse_args():
    parser = argparse.ArgumentParser(description="Browse and play recorded samples.")
    parser.add_argument("--category", choices=["wakeword", "not-wakeword"],
                        help="Filter files by category")
    parser.add_argument("--delete", action="store_true", help="Delete file after playback")
    parser.add_argument("--export", metavar="FOLDER", help="Copy file to folder after playback")
    return parser.parse_args()

def main():
    args = parse_args()
    browse(category=args.category, delete=args.delete, export_path=args.export)
