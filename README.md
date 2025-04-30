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

## 🗂 Directory Structure
/project-root
│
├── app_multiturn.py               # Main Flask application
├── requirements.txt               # Python dependencies
│
├── faiss_search_disease.py        # FAISS disease retrieval module
├── vector_encoder.py              # Vector encoder (handles MacBERT/English models)
├── dynamic_question_manager.py    # Symptom-level dialogue state machine
├── diagnosis_engine.py            # Top-1 scoring logic for diagnosis
├── hospital_recommender.py        # Country-aware hospital recommender
├── symptom_mapping_loader.py      # Loader for symptom-disease mappings
│
├── static/
│   ├── index.js                   # Frontend interaction logic
│   └── style.css                  # UI styles
│
├── templates/
│   └── index.html                 # Main frontend UI
│
├── data/
│   ├── hospitals_database.json    # Hospital database (US & China)
│   ├── symptom_mapping_top50.json# Top 50 rare diseases with primary/secondary symptoms
│   ├── disease_data_demo.json     # Disease description vectors
│   ├── disease_index_en.faiss     # FAISS index (English)
│   └── disease_index_zh.faiss     # FAISS index (Chinese)

## 🚀 How to Run Locally

### 1. Install Dependencies

```bash
pip install -r requirements.txt







☁️ Cloud Deployment

Platform: <to be filled: e.g., Render, Railway, Replit>
Live URL: <to be filled>
Deployment Notes:

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


