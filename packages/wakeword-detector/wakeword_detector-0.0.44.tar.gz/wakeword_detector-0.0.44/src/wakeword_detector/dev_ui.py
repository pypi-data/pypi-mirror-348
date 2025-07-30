import os
import webbrowser
import matplotlib.pyplot as plt
import numpy as np
import librosa
from flask import Flask, render_template, send_from_directory, request, redirect, url_for
from pathlib import Path
from werkzeug.utils import secure_filename
from datetime import datetime  # if needed for logs
from .extract_features import extract_features
import tempfile
import torch
import soundfile as sf
from .train import WakewordModel

BASE_DIR = Path(__file__).parent

app = Flask(
    __name__,
    template_folder=str(BASE_DIR / "templates"),
    static_folder=str(BASE_DIR / "static")
)

print("🔍 Flask template search path:", app.jinja_loader.searchpath)

DATA_DIR = Path.home() / "wakeword_project" / "data"
AUDIO_EXTENSIONS = [".wav"]
WAVEFORM_DIR = BASE_DIR / "static" / "waveforms"

def generate_waveform_thumbnail(label, filename):
    wav_path = DATA_DIR / label / filename
    img_dir = WAVEFORM_DIR / label
    img_dir.mkdir(parents=True, exist_ok=True)
    img_path = img_dir / f"{filename}.png"

    if img_path.exists():
        return  # already generated

    try:
        y, sr = librosa.load(wav_path, sr=16000)
        plt.figure(figsize=(3, 1))
        plt.axis("off")
        plt.plot(np.linspace(0, len(y)/sr, len(y)), y, color="black")
        plt.tight_layout(pad=0)
        plt.savefig(img_path, dpi=100)
        plt.close()
    except Exception as e:
        print(f"⚠️ Could not generate waveform for {filename}: {e}")

def list_audio_files():
    files_by_label = {}
    for label_dir in DATA_DIR.iterdir():
        if not label_dir.is_dir():
            continue
        label = label_dir.name
        files = []
        for f in label_dir.iterdir():
            if f.suffix.lower() in AUDIO_EXTENSIONS:
                generate_waveform_thumbnail(label, f.name)
                files.append(f.name)
        files_by_label[label] = sorted(files)
    return files_by_label

@app.route("/")
def index():
    files = list_audio_files()
    wake_count = len(files.get("wakeword", []))
    neg_count = len(files.get("not-wakeword", []))
    return render_template("index.html", files=files, wake_count=wake_count, neg_count=neg_count)

#  🆕 NEW: Return average length of wakeword samples
@app.route("/avg_wakeword_length")
def avg_wakeword_length():
    wakeword_dir = DATA_DIR / "wakeword"
    if not wakeword_dir.is_dir():
        return { "average_seconds": 1.0 }  # fallback

    lengths = []
    for f in wakeword_dir.iterdir():
        if f.suffix.lower() == ".wav" and f.is_file():
            try:
                y, sr = librosa.load(f, sr=None)
                duration = len(y) / sr
                lengths.append(duration)
            except Exception as e:
                print(f"Could not read {f.name}: {e}")
    if not lengths:
        return { "average_seconds": 1.0 }

    avg = sum(lengths) / len(lengths)
    return { "average_seconds": round(avg, 2) }

@app.route("/status")
def status():
    files = list_audio_files()
    return {
        "wake_count": len(files.get("wakeword", [])),
        "neg_count": len(files.get("not-wakeword", []))
    }

@app.route("/files/<label>")
def get_files(label):
    files = list_audio_files()
    if label not in files:
        return { "files": [] }
    return {
        "files": files[label]
    }

@app.route("/models")
def get_models():
    # match the path where you save your model
    model_dir = BASE_DIR.parent / "models"
    model_dir.mkdir(exist_ok=True)
    files = [f.name for f in model_dir.iterdir() if f.is_file()]
    return { "files": sorted(files) }

@app.route("/audio/<label>/<filename>")
def serve_audio(label, filename):
    return send_from_directory(DATA_DIR / label, filename)

@app.route("/delete/<label>/<filename>", methods=["POST"])
def delete_file(label, filename):
    path = DATA_DIR / label / filename
    if path.exists():
        path.unlink()
    return redirect(url_for("index"))

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("file")
    label = request.form.get("label", "wakeword")

    if not file or not file.filename.lower().endswith(".wav"):
        return "❌ Invalid file", 400

    label_dir = DATA_DIR / label
    label_dir.mkdir(parents=True, exist_ok=True)

    safe_name = secure_filename(file.filename)
    dest_path = label_dir / safe_name
    file.save(dest_path)

    generate_waveform_thumbnail(label, safe_name)

    return redirect(url_for("index"))

@app.route("/move", methods=["POST"])
def move_file():
    filename = request.form.get("filename")
    from_label = request.form.get("from_label")
    to_label = request.form.get("to_label")

    if not all([filename, from_label, to_label]):
        return "❌ Invalid move request", 400

    src = DATA_DIR / from_label / filename
    dest_dir = DATA_DIR / to_label
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / filename

    try:
        src.rename(dest)
        generate_waveform_thumbnail(to_label, filename)
    except Exception as e:
        print(f"❌ Move failed: {e}")
        return "❌ Move failed", 500

    return redirect(url_for("index"))

@app.route("/train", methods=["POST"])
def train_model():
    from .train import train_wakeword_model
    from .extract_features import main as extract_features_main

    try:
        print("🔁 Extracting features...")
        extract_features_main()

        print("🧠 Training model...")
        train_wakeword_model()

        return "✅ Training complete", 200
    except Exception as e:
        print(f"❌ Training failed: {e}")
        return f"Training failed: {e}", 500

@app.route("/delete-multiple/<label>", methods=["POST"])
def delete_multiple(label):
    files = request.form.getlist("delete_files")
    deleted = []

    for filename in files:
        path = DATA_DIR / label / filename
        if path.exists():
            path.unlink()
            deleted.append(filename)

    print(f"🗑️ Deleted {len(deleted)} from {label}")
    return redirect(url_for("index"))


@app.route("/detect", methods=["POST"])
def detect():


    try:
        raw_audio = request.files["audio"].read()
        sample_rate = int(request.form["sample_rate"])
        threshold = float(request.form.get("threshold", 0.5))  # default fallback

        # Convert raw buffer to float32 numpy
        audio_data = np.frombuffer(raw_audio, dtype=np.float32)

        # Write as valid .wav file
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            sf.write(tmp.name, audio_data, sample_rate)
            tmp_path = tmp.name

        # Extract MFCC features
        try:
            features = extract_features(tmp_path)
        except Exception as fe:
            print(f"❌ Feature extraction failed: {fe}")
            return { "confidence": 0.0, "label": "not-wakeword" }

        os.unlink(tmp_path)  # Cleanup temp file

        # Load latest model
        model_dir = BASE_DIR.parent / "models"
        model_path = sorted(model_dir.glob("*.pth"))[-1]
        model = WakewordModel()
        model.load_state_dict(torch.load(model_path))
        model.eval()

        input_tensor = torch.tensor(features, dtype=torch.float32).unsqueeze(0)

        with torch.no_grad():
            output = model(input_tensor).item()

        label = "wakeword" if output > threshold else "not-wakeword"
        print(f"🔍 Detection: {label} (confidence={output:.2f})")

        if output > threshold:
            debug_dir = BASE_DIR / "static" / "detection_snippets"
            debug_dir.mkdir(parents=True, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            debug_filename = debug_dir / f"{timestamp}.wav"
            sf.write(debug_filename, audio_data, sample_rate, subtype='PCM_16')

            meta_file = debug_dir / f"{timestamp}.txt"
            with open(meta_file, "w") as f:
                f.write(f"confidence={round(output, 4)}\nlabel={label}")
        # Generate waveform thumbnail
        try:
            y, sr = librosa.load(debug_filename, sr=16000)
            plt.figure(figsize=(3, 1))
            plt.axis("off")
            plt.plot(np.linspace(0, len(y)/sr, len(y)), y, color="black")
            plt.tight_layout(pad=0)
            plt.savefig(debug_filename.with_suffix(".png"), dpi=100)
            plt.close()
        except Exception as e:
            print(f"⚠️ Could not render waveform for {debug_filename.name}: {e}")


        return { "confidence": round(output, 4), "label": label }

    except Exception as e:
        print(f"❌ Detection error: {e}")
        return { "confidence": 0.0, "label": "not-wakeword" }

@app.route("/detections")
def get_detections():
    folder = BASE_DIR / "static" / "detection_snippets"
    if not folder.exists():
        return { "items": [] }

    items = []
    for f in sorted(folder.glob("*.wav"), reverse=True):
        txt = f.with_suffix(".txt")
        conf = "?"
        label = "unknown"
        if txt.exists():
            with open(txt) as tf:
                lines = tf.readlines()
                for line in lines:
                    if "confidence=" in line:
                        conf = line.strip().split("=")[-1]
                    if "label=" in line:
                        label = line.strip().split("=")[-1]

        # Look for waveform image
        png_path = f.with_suffix(".png")
        waveform = f"/static/detection_snippets/{png_path.name}" if png_path.exists() else None

        items.append({
            "audio": f"/static/detection_snippets/{f.name}",
            "timestamp": f.stem,
            "confidence": conf,
            "label": label,
            "waveform": waveform
        })

    return { "items": items }


@app.route("/promote-detection", methods=["POST"])
def promote_detection():
    from_label = "detection_snippets"
    filename = request.form.get("filename")
    new_label = request.form.get("label")  # "wakeword" or "not-wakeword"

    if not filename or new_label not in ["wakeword", "not-wakeword"]:
        return "❌ Invalid request", 400

    src_path = BASE_DIR / "static" / from_label / filename
    if not src_path.exists():
        return "❌ File not found", 404

    # Move to training set
    label_dir = DATA_DIR / new_label
    label_dir.mkdir(parents=True, exist_ok=True)
    dest_path = label_dir / filename
    src_path.rename(dest_path)

    # Also remove associated .txt metadata
    txt_path = src_path.with_suffix(".txt")
    if txt_path.exists():
        txt_path.unlink()

    return "✅ Promoted and cleaned up", 200

@app.route("/delete-detection/<timestamp>", methods=["POST"])
def delete_detection(timestamp):
    folder = BASE_DIR / "static" / "detection_snippets"
    wav = folder / f"{timestamp}.wav"
    txt = folder / f"{timestamp}.txt"

    deleted = False
    if wav.exists():
        wav.unlink()
        deleted = True
    if txt.exists():
        txt.unlink()

    return ("✅ Deleted", 200) if deleted else ("❌ Not found", 404)


def main():
    try:
        print("🌐 Launching Wakeword Web UI at http://localhost:5000 ...")
        webbrowser.open("http://localhost:5000")
        app.run(debug=True)
    except Exception as e:
        print(f"⚠️ Failed to launch web UI: {e}")
        print("👉 You can still use the CLI to interact with your project.")

if __name__ == "__main__":
    main()
