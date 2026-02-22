<img width="2906" height="1630" alt="image" src="https://github.com/user-attachments/assets/c15b17c0-812e-4180-905d-2210b1b6197f" />


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
     →
Signal Parser
     →
SQLite Storage
     →
Momentum Ranking Engine
     →
FastAPI Backend
     →
Streamlit Dashboard

🌐 Live Demo

Dashboard:
https://vc-momentum-intelligence.streamlit.app

API Documentation:
https://vc-momentum-api.onrender.com/docs

⚙️ Local Setup

Python 3.9+ recommended.

	•	Clone the repository from https://github.com/Manjil-code/vc-momentum-engine
	•	Navigate to the cloned directory: cd vc-momentum-engine
	•	Install dependencies using pip install -r requirements.txt
	•	Run the ingestion script: python ingest.py
	•	Start the backend server using uvicorn api.main:app —reload
	•	Launch the dashboard using streamlit run dashboard.py






