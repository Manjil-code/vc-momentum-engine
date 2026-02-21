from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from scout.ranking import MomentumRanking

app = FastAPI(
    title="VC Momentum Intelligence API",
    description="AI-powered startup momentum tracking and anomaly detection engine",
    version="2.0"
)

# ----------------------------------------
# CORS (Future frontend support)
# ----------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------------------
# Health Check
# ----------------------------------------

@app.get("/")
def health():
    return {
        "status": "running",
        "service": "VC Momentum Intelligence API",
        "version": "2.0"
    }

# ----------------------------------------
# Rankings
# ----------------------------------------

@app.get("/rankings")
def get_rankings():
    try:
        df = MomentumRanking.compute()
        return df.to_dict(orient="records")
    except Exception as e:
        return {"error": str(e)}

# ----------------------------------------
# Sector Momentum
# ----------------------------------------

@app.get("/sectors")
def get_sectors():
    try:
        df = MomentumRanking.sector_momentum()
        return df.to_dict(orient="records")
    except Exception as e:
        return {"error": str(e)}

# ----------------------------------------
# Region Momentum
# ----------------------------------------

@app.get("/regions")
def get_regions():
    try:
        df = MomentumRanking.region_momentum()
        return df.to_dict(orient="records")
    except Exception as e:
        return {"error": str(e)}

# ----------------------------------------
# Breakout Candidates
# ----------------------------------------

@app.get("/breakouts")
def get_breakouts():
    try:
        df = MomentumRanking.breakout_candidates()
        return df.to_dict(orient="records")
    except Exception as e:
        return {"error": str(e)}

# ----------------------------------------
# Statistical Anomalies
# ----------------------------------------

@app.get("/anomalies")
def get_anomalies():
    try:
        df = MomentumRanking.statistical_anomalies()
        return df.to_dict(orient="records")
    except Exception as e:
        return {"error": str(e)}

