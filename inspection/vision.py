"""Vision module — Detector abstraction

- Keeps a clear interface so you can drop-in a YOLO/OpenCV detector later.
- By default returns deterministic mock detections to make demos reproducible.
"""
from PIL import Image
import hashlib
import random


class Detector:
    """Detector abstraction. Replace internals with a real model loader/detector.

    Methods:
    - load_model(path): load model weights (stub)
    - detect(pil_image): return list of detections

    Detection format (per item):
      {"label": str, "confidence": float, "bbox": [x, y, w, h]}  # bbox in pixels
    """

    SUPPORTED = ["crack", "corrosion", "leak"]

    def __init__(self, model_path: str = None, use_mock: bool = True):
        self.model_path = model_path
        self.use_mock = use_mock
        self.model = None
        if not use_mock:
            self.load_model(model_path)

    def load_model(self, path: str):
        """Load your real model here (YOLO, TorchScript, OpenVINO, etc.).
        Keep the detect() signature the same so the rest of the system is unchanged.
        """
        raise NotImplementedError("Integrate a real model here (YOLO/OpenCV).")

    def detect(self, pil_image: Image.Image):
        """Detect defects in a PIL image.

        For demo purposes this returns deterministic mock detections derived from
        the image bytes (so the same image -> same detections).
        """
        if self.use_mock:
            return self._mock_detect(pil_image)
        # if a model is loaded, call it here and convert outputs to the detection schema
        raise NotImplementedError("Model-backed detection not implemented.")

    # --------------------- Mock logic (demo) ---------------------
    def _mock_detect(self, pil_image: Image.Image):
        # Deterministic seed from the image content
        buf = pil_image.tobytes()[:1024]
        h = hashlib.sha1(buf).hexdigest()
        seed = int(h[:8], 16)
        rng = random.Random(seed)

        w, h_img = pil_image.size
        detections = []

        # Decide how many defects (0..3)
        n = rng.choices([0, 1, 2, 3], weights=[20, 50, 20, 10])[0]
        for i in range(n):
            label = rng.choice(self.SUPPORTED)
            confidence = round(rng.uniform(0.6, 0.98), 2)

            # bbox size depends on defect type (approx)
            if label == "crack":
                bw = int(w * rng.uniform(0.08, 0.4))
                bh = int(h_img * rng.uniform(0.01, 0.05))
            elif label == "corrosion":
                bw = int(w * rng.uniform(0.05, 0.25))
                bh = int(h_img * rng.uniform(0.05, 0.25))
            else:  # leak
                bw = int(w * rng.uniform(0.05, 0.18))
                bh = int(h_img * rng.uniform(0.05, 0.12))

            x = int(rng.uniform(0, max(1, w - bw)))
            y = int(rng.uniform(0, max(1, h_img - bh)))

            detections.append({
                "label": label,
                "confidence": confidence,
                "bbox": [x, y, bw, bh],
            })

        return detections
