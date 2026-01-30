"""Industrial Inspection — Flask API (demo-ready, modular)

Endpoints
- GET  /health        -> service status
- POST /analyze       -> accepts multipart image (field: `image`) or JSON {"use_sample": true}

Design notes
- Vision and reasoning are modular: replace the mock detector with a YOLO/OpenCV implementation by implementing Detector.load_model() and Detector.detect().
- Returns JSON with detections, SOP mappings, recommendations and a base64 annotated image for quick demos.
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import io
import base64

from inspection.vision import Detector
from inspection.reasoning import Reasoner
from inspection.utils import pil_image_to_base64, draw_detections

APP_VERSION = "0.1.0"

app = Flask(__name__, static_url_path="/static")
CORS(app)

# Initialize modules (mock by default; easy to replace with real model)
detector = Detector(use_mock=True)
reasoner = Reasoner()


@app.route("/health", methods=["GET"])
def health():
    """Health check for orchestration and demos."""
    return jsonify({"status": "ok", "version": APP_VERSION})


@app.route("/analyze", methods=["POST"])
def analyze():
    """Main analysis endpoint.

    Accepts multipart/form-data with `image` file, or JSON {"use_sample": true}.
    Returns structured JSON with:
      - detections: [{label, confidence, bbox: [x,y,w,h]}]
      - analysis: {severity, sop_mappings, recommendations}
      - annotated_image: base64-encoded PNG (useful for quick demos)
    """
    try:
        # Load image from upload or use bundled sample
        if request.content_type and request.content_type.startswith("multipart/") and "image" in request.files:
            file = request.files["image"]
            image = Image.open(file.stream).convert("RGB")
        else:
            # allow JSON body with use_sample flag for quick demos
            body = request.get_json(silent=True) or {}
            use_sample = body.get("use_sample", False)
            if use_sample:
                # load sample image shipped with the frontend
                image = Image.open("static/images/sample_panel.svg").convert("RGBA").convert("RGB")
            else:
                return jsonify({"error": "No image provided. Send multipart form with field 'image' or JSON {\"use_sample\": true}."}), 400

        # Run detection (mock or real)
        detections = detector.detect(image)

        # Run reasoning / SOP mapping
        analysis = reasoner.analyze(detections, image.size)

        # Create an annotated image for the UI (PIL -> base64)
        annotated = draw_detections(image, detections, analysis)
        annotated_b64 = pil_image_to_base64(annotated)

        return jsonify({
            "detections": detections,
            "analysis": analysis,
            "annotated_image": annotated_b64,
        })

    except Exception as e:
        # Keep errors readable for demo — in production log and return sanitized messages
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # Development server (use gunicorn or uvicorn for production)
    app.run(host="0.0.0.0", port=5000, debug=True)
