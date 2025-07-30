import torch
from wakeword_detector.train import WakewordModel


# Load your trained PyTorch model
model = WakewordModel()
model.load_state_dict(torch.load("wakeword_model.pth", map_location="cpu"))
model.eval()

# Dummy input that matches the shape (1, 13 MFCC features)
dummy_input = torch.randn(1, 13)

# Export to ONNX
torch.onnx.export(
    model,
    dummy_input,
    "wakeword_model.onnx",
    input_names=["input"],
    output_names=["output"],
    dynamic_axes={"input": {0: "batch_size"}},
    opset_version=11
)

print("✅ Export complete: wakeword_model.onnx")
