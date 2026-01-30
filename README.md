
# INSPECT-AI: Explainable Edge AI for Industrial Safety

INSPECT-AI is an AI-powered industrial inspection system that performs real-time defect detection, reasoning, and safety compliance mapping using computer vision and explainable AI techniques.

This project demonstrates how Edge AI and Vision-Language Reasoning can be combined to improve industrial safety, reduce manual inspections, and enable data-driven maintenance decisions.

---

## 🚀 Features

- Real-time industrial defect detection (Cracks, Corrosion, Leaks)
- Edge-based processing with low latency
- Explainable AI reasoning with severity classification
- SOP and ISO safety standard mapping
- Actionable maintenance recommendations
- Interactive web dashboard
- Automated inspection reporting
- Scalable and modular architecture

---

## 🏗️ Project Architecture

```
industrial-inspection-ai/
│
├── backend/
│   ├── app.py            # Flask backend API
│   ├── vision.py         # Defect detection logic
│   ├── reasoning.py     # Severity + SOP reasoning
│   ├── utils.py         # Helper functions
│   └── requirements.txt
│
├── frontend/
│   ├── index.html        # Dashboard UI
│   ├── style.css         # Styling
│   └── script.js         # Frontend logic
│
└── README.md
```

---

## 🧠 How It Works

1. Cameras capture live industrial asset footage.
2. Edge AI detects visual anomalies in real time.
3. Reasoning engine classifies defect severity.
4. Detected defects are mapped to SOP/ISO standards.
5. Actionable recommendations are generated.
6. Results are displayed on the dashboard and logged for audits.

---

## ⚙️ Tech Stack

### Backend
- Python
- Flask
- OpenCV
- NumPy

### Frontend
- HTML
- CSS
- JavaScript

### AI & Logic
- Computer Vision
- Explainable AI
- Rule-based reasoning (extendable to LLMs)

---

## ▶️ How to Run the Project

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/inspect-ai.git
cd inspect-ai
```

### 2. Run Backend
```bash
cd backend
pip install -r requirements.txt
python app.py
```

### 3. Run Frontend
- Open `frontend/index.html` in your browser
- Click **Run Inspection** to see live AI output

---

## 📊 Example Output

```json
{
  "defect": "Crack",
  "confidence": 0.93,
  "location": "Pipeline Joint A",
  "severity": "High",
  "sop_reference": "ISO 15649 – Pressure Piping",
  "recommendation": "Schedule ultrasonic testing within 48 hours"
}
```

---

## 🔐 Safety & Ethics

- No human surveillance or biometric data
- Asset-focused inspection only
- Human-in-the-loop decision making
- Explainable and auditable outputs

---

## 📈 Scalability

- Supports multiple cameras and assets
- Edge-first architecture minimizes cloud dependency
- Easy integration with existing industrial systems
- Extendable to cloud and multi-agent setups

---

## 🌟 Future Enhancements

- YOLOv8 real-time defect detection
- Streamlit dashboard version
- Predictive maintenance analytics
- Multi-agent AI reasoning
- Cloud deployment (AWS / Azure)

---

## 🏆 Ideal For

- Hackathons
- Industrial AI POCs
- Smart manufacturing demos
- Safety compliance solutions

---

## 📄 License

This project is for educational and demonstration purposes.
