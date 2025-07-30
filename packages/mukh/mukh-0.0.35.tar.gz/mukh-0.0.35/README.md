# Mukh

Mukh (मुख, meaning "face" in Sanskrit) is a comprehensive face analysis library that provides unified APIs for various face-related tasks. It simplifies the process of working with multiple face analysis models through a consistent interface.

## Features

- 🎯 **Unified API**: Single, consistent interface for multiple face analysis tasks
- 🔄 **Model Flexibility**: Support for multiple models per task
- 🛠️ **Custom Pipelines**: Optimized preprocessing and model combinations
- 📊 **Evaluator Mode**: Intelligent model recommendations based on your dataset
- 🚀 **Easy to Use**: Simple, intuitive APIs for quick integration

## Currently Supported Tasks

- Face Detection
- Facial Landmark Prediction

## Installation

```bash
pip install mukh
```

## Usage

### Face Detection

```python
import cv2
from mukh.detection import FaceDetector

# Initialize detector
detection_model = "blazeface" # Available models: "blazeface", "mediapipe", "ultralight"
detector = FaceDetector.create(detection_model)

# Detect faces
image_path = "path/to/image.jpg"
faces, annotated_image = detector.detect_with_landmarks(image_path)

# Save output
output_path = "path/to/output.jpg"
cv2.imwrite(output_path, annotated_image)
```

## Contact

For questions and feedback, please open an issue on GitHub.
