import os
import subprocess
import torch
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# If model directory does not exist, run train.py automatically
if not os.path.exists("model") or not os.path.exists("model/model.safetensors"):
    print("Model directory not found. Automatically running train.py...")
    import sys
    subprocess.run([sys.executable, "train.py"], check=True)

app = Flask(__name__)
CORS(app) # Enable CORS for Netlify frontend

THRESHOLD = 0.50 # below this confidence the page says "Not sure"
MAX_CHARS = 200

tokenizer = AutoTokenizer.from_pretrained("model")
model = AutoModelForSequenceClassification.from_pretrained("model")
model.eval()

INFO = {
    "admissions": {
        "title": "Admissions",
        "department": "Admissions Office",
        "contact": "admissions@yourcollege.edu",
        "answer": "Apply online through the college website. Keep your marks memos and ID proof ready."
    },
    "fees": {
        "title": "Fees & Scholarships",
        "department": "Accounts Section",
        "contact": "accounts@yourcollege.edu",
        "answer": "Pay fees on the student portal or at the Accounts counter. Scholarships: same office."
    },
    "exams": {
        "title": "Exams & Results",
        "department": "Examination Cell",
        "contact": "exams@yourcollege.edu",
        "answer": "Timetables, hall tickets and results are on the student portal. Revaluation: Exam Cell."
    },
    "hostel_transport": {
        "title": "Hostel & Transport",
        "department": "Hostel Warden / Transport Office",
        "contact": "hostel@yourcollege.edu",
        "answer": "Apply for hostel rooms at the Warden's office. Bus routes: Transport Office."
    },
    "library": {
        "title": "Library",
        "department": "Central Library",
        "contact": "library@yourcollege.edu",
        "answer": "Borrow books with your library card. Renew online or at the issue counter."
    },
    "placements": {
        "title": "Placements & Internships",
        "department": "Training & Placement Cell",
        "contact": "placements@yourcollege.edu",
        "answer": "Register on the placement portal with your resume. Drive dates are announced by the Cell."
    }
}

@app.route("/")
def home():
    try:
        return render_template("index.html")
    except Exception:
        return jsonify(status="ok", message="College FAQ Classification API running on Render")

@app.route("/health")
def health():
    return jsonify(status="ok", service="college-faq-bert-api")

@app.route("/api/classify", methods=["POST", "OPTIONS"])
def classify():
    if request.method == "OPTIONS":
        return "", 200
        
    data = request.get_json(silent=True) or {}
    text = (data.get("question") or "").strip()
    if not text:
        return jsonify(error="Please type a question."), 400
    if len(text) > MAX_CHARS:
        return jsonify(error=f"Keep it under {MAX_CHARS} characters."), 400
        
    enc = tokenizer(text, truncation=True, max_length=48, return_tensors="pt")
    with torch.no_grad():
        probs = torch.softmax(model(**enc).logits, dim=-1)[0]
        score, idx = torch.max(probs, dim=0)
        key = model.config.id2label[idx.item()]
        info = INFO[key]
        return jsonify(
            category=key,
            title=info["title"],
            confidence=round(score.item(), 4),
            confident=score.item() >= THRESHOLD,
            department=info["department"],
            contact=info["contact"],
            answer=info["answer"]
        )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
