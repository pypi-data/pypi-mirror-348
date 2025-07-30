import os
import asyncio
import websockets
import json
from .detector import WakewordDetector

# Suppress TensorFlow GPU log noise
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"  # Only show critical errors

def get_default_model_path():
    """Check for an existing model file and return the path if found."""
    for filename in ["wakeword_model.h5", "wakeword_model.pth"]:
        if os.path.exists(filename):
            return filename
    return None

async def wakeword_server(detector, websocket, path):
    """Sends wakeword detection probabilities to connected clients (React)."""
    while True:
        detected, probability = detector.detect()
        await websocket.send(json.dumps({
            "wakeword_detected": detected,
            "confidence": probability
        }))
        await asyncio.sleep(0.5)

def main():
    model_path = get_default_model_path()

    if model_path is None:
        print("⚠️ No wakeword model found (expected 'wakeword_model.h5' or 'wakeword_model.pth').")
        print("👉 Run `wakeword-detector start` to record training data and train a model.")
        print("   Or run `wakeword-detector train` if you already have audio samples.")
        return

    print(f"🚀 Serving wakeword model: {model_path}")
    detector = WakewordDetector(model_path)

    start_server = websockets.serve(
        lambda ws, path: wakeword_server(detector, ws, path),
        "0.0.0.0",
        5001
    )

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    main()
