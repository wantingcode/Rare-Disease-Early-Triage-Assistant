# Rare Disease Early Triage Assistant

## 🔍 Project Overview

This project is a bilingual, interactive rare disease triage assistant designed to support early-stage diagnosis. By entering symptoms in natural language, users receive intelligent suggestions of potential rare diseases and suitable hospital recommendations based on a combination of semantic vector search, symptom mapping, and dynamic multi-turn questioning.

## ✅ Key Features

- 🧠 **Natural Language Symptom Understanding** (Chinese + English)
- 🔍 **FAISS-Based Disease Retrieval** using bilingual medical vectors
- 💬 **Dynamic Multi-Turn Symptom Querying** via yes/no bubbles
- 🎯 **Top-1 Disease Confidence Scoring**
- 🏥 **Hospital Recommendation System** (supports both U.S. and China)
- 🌐 **Language Auto-Detection** and bilingual knowledge base


## 🚀 How to Run Locally

1. Install Dependencies

```bash
pip install -r requirements.txt
```
2. Start the App
```bash
python app_multiturn.py
# or for production
gunicorn app_multiturn:app
```
3. Open in Browser
```bash
http://localhost:5001/
```
⚙️ Environment Variables

No special environment variables are required.

📊 Dataset Coverage
	•	🔸 Top 50 globally recognized rare diseases
	•	🔸 Each disease includes bilingual:
	•	1 primary symptom
	•	2 secondary symptoms
	•	🔸 Hospitals support region-filtered recommendation

👩‍⚕️ Future Improvements
	•	Add patient profile memory
	•	Add image/OCR upload support
	•	Expand database to include 200+ diseases

   
