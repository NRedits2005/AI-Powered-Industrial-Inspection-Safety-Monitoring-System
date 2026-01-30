"""Reasoning module

- Classifies severity from detections
- Maps defects to ISO / SOP references (example mappings included)
- Produces actionable recommendations

Keep this deterministic and easy to extend with a rules engine or LLM later.
"""
from typing import List, Dict, Any


class Reasoner:
    """Simple rule-based reasoner for industrial defects.

    Extend points:
    - Add more ISO mappings
    - Replace rules with a configurable rules engine or LLM prompts
    """

    # Example SOP/ISO mappings (illustrative — adapt to your org)
    SOP_DB = {
        "crack": {
            "iso": "ISO 6508",
            "sop": "Inspect crack length; measure propagation; schedule NDT (ultrasonic).",
            "priority": "P2",
        },
        "corrosion": {
            "iso": "ISO 9227",
            "sop": "Assess corrosion depth/area; clean and apply corrosion inhibitor; consider replacement.",
            "priority": "P2",
        },
        "leak": {
            "iso": "ISO 5167",
            "sop": "Isolate line; perform pressure test; immediate repair if active leak.",
            "priority": "P1",
        },
    }

    def __init__(self):
        pass

    def analyze(self, detections: List[Dict[str, Any]], image_size=(0, 0)) -> Dict[str, Any]:
        """Return a structured analysis for the given detections.

        Output example:
        {
          "summary": {counts...},
          "severity": "high|medium|low",
          "sop_mappings": [...],
          "recommendations": [...]
        }
        """
        summary = {"total": len(detections)}
        counts = {}
        sop_mappings = []
        recs = []

        for d in detections:
            lbl = d["label"]
            counts[lbl] = counts.get(lbl, 0) + 1

            # map to SOP/ISO
            meta = self.SOP_DB.get(lbl, {})
            sop_mappings.append({
                "label": lbl,
                "iso": meta.get("iso", "N/A"),
                "sop": meta.get("sop", "Refer engineering SOP."),
                "priority": meta.get("priority", "P3"),
            })

            # severity heuristics (simple rules)
            sev = self._estimate_severity(d, image_size)
            recs.extend(self._recommendations_for(lbl, sev, d))

        # overall severity: highest among detections
        overall = self._aggregate_severity(detections, image_size)

        return {
            "summary": {**summary, **counts},
            "severity": overall,
            "sop_mappings": sop_mappings,
            "recommendations": recs,
        }

    # ----------------- Internal rules -----------------
    def _estimate_severity(self, detection: Dict, image_size) -> str:
        lbl = detection["label"]
        x, y, w, h = detection["bbox"]
        img_w, img_h = image_size

        # Normalize area ratio
        area_ratio = (w * h) / max(1, img_w * img_h)

        if lbl == "leak":
            # leaks are high by default
            if detection.get("confidence", 0) > 0.7:
                return "high"
            return "medium"

        if lbl == "crack":
            # long cracks -> higher severity
            length_ratio = max(w, h) / max(1, max(img_w, img_h))
            if length_ratio > 0.25 or area_ratio > 0.02:
                return "high"
            if length_ratio > 0.08:
                return "medium"
            return "low"

        if lbl == "corrosion":
            if area_ratio > 0.06:
                return "high"
            if area_ratio > 0.02:
                return "medium"
            return "low"

        return "low"

    def _recommendations_for(self, label: str, severity: str, detection: Dict) -> List[str]:
        base = self.SOP_DB.get(label, {})
        recs = []
        if severity == "high":
            recs.append(f"{label}: Immediate action — follow SOP: {base.get('sop')}")
            recs.append("Schedule shutdown and NDT / specialist inspection within 24 hours.")
        elif severity == "medium":
            recs.append(f"{label}: Repair or patch and inspect; follow SOP: {base.get('sop')}")
            recs.append("Monitor weekly and re-inspect with higher-fidelity sensors.")
        else:
            recs.append(f"{label}: Document and schedule maintenance per SOP: {base.get('sop')}")

        # add a data-driven recommendation
        if detection.get("confidence", 0) < 0.75:
            recs.append("Confidence is moderate — capture higher-resolution image for verification.")

        return recs

    def _aggregate_severity(self, detections, image_size):
        order = {"low": 0, "medium": 1, "high": 2}
        worst = "low"
        for d in detections:
            s = self._estimate_severity(d, image_size)
            if order[s] > order[worst]:
                worst = s
        return worst
