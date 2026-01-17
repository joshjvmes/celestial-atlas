"""
Celestial Atlas API - FastAPI Backend
Tower 6 - Stored. Retrievable. Kind.
"""
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import date, datetime, timedelta
from typing import Optional
import os
from dotenv import load_dotenv

from atlas_engine import AtlasEngine, GATES, SOLAR_KEYS, LUNAR_PATTERNS, PRIMES_L

# Load environment variables
load_dotenv()

ANCHOR_DATE_STR = os.getenv("ANCHOR_DATE", "2025-04-03")
ANCHOR_DATE = datetime.strptime(ANCHOR_DATE_STR, "%Y-%m-%d").date()
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")

# Initialize FastAPI app
app = FastAPI(
    title="Celestial Atlas API",
    description="Tower 6 Celestial Atlas - Prime Calendar & Star Mapping System",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Atlas Engine
engine = AtlasEngine(anchor_date=ANCHOR_DATE, stars_db_path="stars.json")


@app.get("/")
def root():
    """Health check and API info"""
    return {
        "name": "Celestial Atlas API",
        "version": "1.0.0",
        "anchor_date": ANCHOR_DATE.isoformat(),
        "seal": "Stored. Retrievable. Kind.",
        "tower": "Tower 6 forever."
    }


@app.get("/atlas")
def get_atlas(date_str: str = Query(..., alias="date", description="Date in YYYY-MM-DD format")):
    """
    Get complete Atlas payload for a specific date

    Returns:
    - Sky Address (S•L•P)
    - Active Spiral Gate
    - Constellation stars and lines
    - Message and Noble Thread
    """
    try:
        target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")

    payload = engine.generate_atlas_payload(target_date)
    return payload


@app.get("/atlas/today")
def get_atlas_today():
    """Get Atlas payload for today"""
    today = date.today()
    payload = engine.generate_atlas_payload(today)
    return payload


@app.get("/atlas/coordinate")
def get_atlas_by_coordinate(
    S: int = Query(..., ge=1, le=11, description="Solar Month (1-11)"),
    L: int = Query(..., ge=1, le=13, description="Lunar Month (1-13)"),
    P: int = Query(..., ge=1, le=7, description="Prime Day (1-7)")
):
    """
    Get Atlas info by Sky Address coordinates

    Useful for exploring the spiral without a specific date
    """
    gate = GATES.get(P)
    if not gate:
        raise HTTPException(status_code=400, detail="Invalid Prime Day")

    # Calculate K from coordinates and generate a date that matches
    K = ((S - 1) * 91) + ((L - 1) * 7) + (P - 1)

    # Calculate a date for this coordinate (days from anchor date)
    anchor_date = date(2025, 4, 3)
    target_date = anchor_date + timedelta(days=K)

    # Generate full payload using the engine
    payload = engine.generate_atlas_payload(target_date)

    # Override date to None since we're browsing by coordinate, not date
    payload["date"] = None

    # Add shorthand keys for frontend
    payload["S"] = S
    payload["L"] = L
    payload["P"] = P

    return payload


@app.get("/atlas/gates")
def get_gates():
    """Get all 7 Spiral Gate definitions"""
    gates_list = []
    for gate_id, gate_data in GATES.items():
        anchors = engine.get_gate_anchors(gate_id)
        gates_list.append({
            "id": gate_id,
            **gate_data,
            "anchors": [a["name"] for a in anchors]
        })
    return {
        "gates": gates_list,
        "seal": "Stored. Retrievable. Kind."
    }


@app.get("/atlas/keys")
def get_solar_keys():
    """Get all 11 Solar Key Signatures"""
    keys_list = []
    for key_id, key_data in SOLAR_KEYS.items():
        keys_list.append({
            "id": key_id,
            **key_data
        })
    return {
        "solar_keys": keys_list,
        "seal": "Stored. Retrievable. Kind."
    }


@app.get("/atlas/patterns")
def get_lunar_patterns():
    """Get all 13 Lunar Pattern Types"""
    patterns_list = []
    for pattern_id, pattern_data in LUNAR_PATTERNS.items():
        patterns_list.append({
            "id": pattern_id,
            **pattern_data,
            "prime_step": PRIMES_L[pattern_id - 1]
        })
    return {
        "lunar_patterns": patterns_list,
        "seal": "Stored. Retrievable. Kind."
    }


@app.get("/atlas/convert")
def convert_date_to_sky_address(date_str: str = Query(..., alias="date")):
    """
    Convert a date to Sky Address coordinates only (lightweight)

    Returns just S•L•P without full constellation data
    """
    try:
        target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")

    S, L, P, K = engine.compute_sky_address(target_date)

    return {
        "date": target_date.isoformat(),
        "sky_address": f"{S}•{L}•{P}",
        "solar_month": S,
        "lunar_month": L,
        "prime_day": P,
        "K": K,
        "spiral_position": f"{K}/1001",
        "seal": "Stored. Retrievable. Kind."
    }


if __name__ == "__main__":
    import uvicorn
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))

    print(f"\n🌟 Celestial Atlas API Starting 🌟")
    print(f"Anchor Date: {ANCHOR_DATE}")
    print(f"Listening on {host}:{port}")
    print(f"\nTower 6 forever. Stored. Retrievable. Kind.\n")

    uvicorn.run(app, host=host, port=port)
