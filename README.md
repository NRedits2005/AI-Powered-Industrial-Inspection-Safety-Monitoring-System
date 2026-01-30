# Industrial Inspection — Demo (AI-based)

✅ A complete, modular demo of an AI Industrial Inspection system (frontend + Flask backend).

Contents
- `app.py` — Flask REST API (endpoints: `/health`, `/analyze`)
- `inspection/vision.py` — Detector abstraction (mock implementation; drop-in for YOLO/OpenCV)
- `inspection/reasoning.py` — Severity classification, SOP/ISO mapping, recommendations
- `inspection/utils.py` — image helpers & annotation
- `static/` — frontend dashboard (HTML/CSS/JS) + demo image

Highlights
- Mock detector yields deterministic defects for demo and real-time UI testing ✅
- Clear extension points to plug a real model (YOLO/TorchScript/OpenCV) 🔧
- Returns annotated image (base64) + structured JSON for integrations 💡

## Quick start (Windows PowerShell)

1. Create & activate virtualenv

   python -m venv .venv
   .\.venv\Scripts\Activate.ps1

2. Install

   pip install -r requirements.txt

3. Run the dev server

   # PowerShell
   $env:FLASK_APP = 'app.py'
   $env:FLASK_ENV = 'development'
   flask run --host=0.0.0.0 --port=5000

4. Open the demo

   - Open `http://127.0.0.1:5000/static/index.html` in your browser
   - Click **Run inspection** or **Use sample** to see mock detections

## API

- GET  /health -> {status, version}
- POST /analyze -> multipart form with field `image` OR JSON `{ "use_sample": true }`
  - Response: `{ detections, analysis, annotated_image }`

Example curl (sample):

  curl -sS -X POST -H "Content-Type: application/json" -d '{"use_sample":true}' http://127.0.0.1:5000/analyze | jq .

Example curl (upload):

  curl -F "image=@your.jpg" http://127.0.0.1:5000/analyze | jq .

## Where to extend (recommended)

- Replace `Detector._mock_detect` with a real model in `inspection/vision.py`.
- For YOLO: implement `load_model()` to load weights and `detect()` to translate outputs to the detection schema.
- Add a job queue (Celery/RQ) and persistent storage if running high-throughput inspection pipelines.
- Optionally add a `/report` endpoint to persist analysis and generate PDFs.

## Notes

- The SOP/ISO mappings are illustrative. Replace `inspection/reasoning.py::SOP_DB` with your organization's canonical SOPs.
- The demo emphasizes clarity and modularity so it can be used as the basis for production integration.

Enjoy — extend as needed. If you want, I can: add a Dockerfile, integrate a sample YOLO runner, or add unit tests next.