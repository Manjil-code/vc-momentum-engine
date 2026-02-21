VC Momentum Intelligence Platform 🚀

AI-powered startup signal ranking engine that collects, scores, and ranks companies based on momentum signals from public sources.

🔍 Features

	•	Scalable signal ingestion
	•	Time-decay momentum scoring
	•	Sector & region analytics
	•	Statistical anomaly detection (Z-score)
	•	REST API built with FastAPI
	•	Interactive dashboard using Streamlit
	•	Cloud deployment (Render + Streamlit Cloud)

Architecture

Data Sources
     ↓
Signal Parser
     ↓
SQLite Storage
     ↓
Momentum Ranking Engine
     ↓
FastAPI Backend
     ↓
Streamlit Dashboard

🌐 Live Demo

Dashboard:
https://vc-momentum-intelligence.streamlit.app

API Documentation:
https://vc-momentum-api.onrender.com/docs

⚙️ Local Setup

Python 3.9+ recommended.

Clone the repository:

git clone https://github.com/Manjil-code/vc-momentum-engine
cd vc-momentum-engine

Install dependencies:

pip install -r requirements.txt

Run ingestion:

python ingest.py

Start backend:

uvicorn api.main:app --reload

Launch dashboard:

streamlit run dashboard.py

