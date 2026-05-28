import numpy as np
import torch
from facenet_pytorch import MTCNN, InceptionResnetV1
from PIL import Image
from torchvision import transforms


DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

_transform = transforms.Compose([
    transforms.Resize((160, 160)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5]),
])


class FaceRecognizer:
    def __init__(self):
        self.detector = MTCNN(keep_all=True, device=DEVICE, min_face_size=60)
        self.model = InceptionResnetV1(pretrained="vggface2").eval().to(DEVICE)

    def detect(self, rgb_frame: np.ndarray):
        """Return bounding boxes or None."""
        boxes, _ = self.detector.detect(rgb_frame)
        return boxes

    def embed(self, image: Image.Image) -> np.ndarray:
        """Compute a normalised embedding for a face image."""
        tensor = _transform(image).unsqueeze(0).to(DEVICE)
        with torch.no_grad():
            vec = self.model(tensor).cpu().numpy().flatten()
        return vec / np.linalg.norm(vec)

    def crop_face(self, rgb_frame: np.ndarray, box) -> Image.Image | None:
        """Crop a face from a frame given a bounding box."""
        x1, y1, x2, y2 = map(int, box)
        x1, y1 = max(0, x1), max(0, y1)
        crop = rgb_frame[y1:y2, x1:x2]
        if crop.size == 0:
            return None
        return Image.fromarray(crop).convert("RGB")

    def identify(self, embedding, known, threshold=0.70):
        best_name, best_score = "Unknown", threshold
        for name, ref in known.items():
            score = float(np.dot(embedding, ref))
            if score > best_score:
                best_name, best_score = name, score
        return best_name, best_score
