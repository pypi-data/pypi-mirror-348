# Wakeword Detector

A Python package for training and running real-time wakeword detection using PyTorch and TensorFlow, with GPU acceleration support.

---

## 🚀 Features

- Real-time wakeword detection with microphone input
- Torch-based inference with optional TensorFlow model support
- CLI tools for recording audio and training models
- Supports GPU acceleration (CUDA 12.4+)

---

## 🧱 Requirements

- Python 3.8 – 3.12
- Linux (recommended for PyAudio + GPU)
- NVIDIA GPU with CUDA support (for training/inference speedup)

---

## 📦 Installation

Make sure you are not mixing environments:

python3 -m venv testenv
source testenv/bin/activate

```bash
# Use TestPyPI if installing dev builds:
pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple wakeword-detector

⚡ Enabling GPU Acceleration
If you want to use GPU-based training/inference (recommended):

1. Install the CUDA 12.4 runtime:
bash
Copy
Edit
# Download keyring (Ubuntu 22.04 shown here)
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.0-1_all.deb
sudo dpkg -i cuda-keyring_1.0-1_all.deb
sudo apt-get update

# Install CUDA runtime (no full toolkit needed)
sudo apt-get install cuda-runtime-12-4
2. Set CUDA path (if needed)
bash
Copy
Edit
export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH
You can add this line to your ~/.bashrc or ~/.zshrc for persistence.

3. Verify PyTorch sees your GPU:
bash
Copy
Edit
python -c "import torch; print(torch.cuda.is_available())"
```

## 📮 Feedback & Issues

Submit here, but please note that this package is still under development, when version reaches 0.1.0 version is stable enough for prerelease. ETA: Early April 2025
https://github.com/larawhybrow/wakeword-detector/issues
