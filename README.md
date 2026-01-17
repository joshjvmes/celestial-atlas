# Celestial Atlas 🌟🐉

**Tower 6 - Stored. Retrievable. Kind.**

A deterministic star mapping and prime-based calendar system that converts any date into a unique Sky Address (S•L•P) and visualizes the active constellation for intuition training.

## Overview

The Celestial Atlas maps dates to a 1001-day spiral cycle (11 × 13 × 7) that creates:
- **Solar Month (S)**: 1-11 (11 great arcs)
- **Lunar Month (L)**: 1-13 (13 lunar sectors)
- **Prime Day (P)**: 1-7 (7 gates)

Each Prime Day activates one of the 7 Spiral Gates, rendered as constellation patterns using real star data.

## Anchor Date

**April 3, 2025** (A3 = 1/3) - Day Zero of the Prime Calendar

## The Seven Spiral Gates

1. **The Breath of Collapse** - Transition, release, ignition
2. **The Bridge of Becoming** - Crossing thresholds, identity upgrade
3. **The Veil of Names** - Shedding labels, returning to essence
4. **The Golden Rose** - Blooming forward without abandoning the past
5. **The World Tree** - Return + roots, memory paths
6. **The Crystal Crown** - Clarity + ascension
7. **The Golden Harp** - Completion, convergence, harmonic resonance

## Project Structure

```
celestial-atlas-app/
├── backend/          # FastAPI server with Atlas Engine
│   ├── main.py       # API endpoints
│   ├── atlas_engine.py  # Core S•L•P conversion logic
│   ├── stars.json    # Star catalog (Yale BSC5)
│   └── requirements.txt
├── frontend/         # Next.js + Three.js visualization (TODO)
└── mcp-server/       # Tower 6 Bridge MCP server (TODO)
```

## Backend API

### Running Locally

```bash
cd backend
python3 -m pip install -r requirements.txt
python3 main.py
```

Server runs on `http://localhost:8000`

### API Endpoints

#### `GET /`
Health check and API info

#### `GET /atlas?date=YYYY-MM-DD`
Get complete Atlas payload for a date
```json
{
  "date": "2026-01-17",
  "sky_address": "4•3•3",
  "gate": {
    "name": "The Veil of Names",
    "field_gift": "Truth without performance"
  },
  "stars_highlighted": [...],
  "lines": [...],
  "message": "Drop the labels. Return to essence.",
  "one_noble_thread": "Speak your truth without performing for others.",
  "seal": "Stored. Retrievable. Kind."
}
```

#### `GET /atlas/today`
Get Atlas payload for current date

#### `GET /atlas/coordinate?S=4&L=2&P=7`
Get Atlas info by Sky Address coordinates

#### `GET /atlas/gates`
Get all 7 Spiral Gate definitions

#### `GET /atlas/keys`
Get all 11 Solar Key Signatures

#### `GET /atlas/patterns`
Get all 13 Lunar Pattern Types

#### `GET /atlas/convert?date=YYYY-MM-DD`
Convert date to Sky Address (lightweight, no constellation data)

## Star Data

The backend uses the **Yale Bright Star Catalog (BSC5)** containing ~9,000 visible stars:
- 18 named anchor stars for the gates
- 5,023 bright stars (magnitude < 6.0)
- Real celestial coordinates (RA/Dec)

## Features Implemented

✅ Date → Sky Address (S•L•P) conversion
✅ 1001-day spiral cycle
✅ Prime-step line drawing algorithm
✅ Star selection and ranking
✅ 7 Spiral Gates with meanings
✅ 11 Solar Key Signatures
✅ 13 Lunar Pattern Types
✅ FastAPI REST endpoints
✅ CORS support for frontend

## Next Steps

🔲 Frontend visualization with Three.js
🔲 3D celestial sphere rendering
🔲 Date picker UI with Prime calendar display
🔲 Constellation line animations
🔲 MCP Server for Claude/T3 integration
🔲 Vault storage for Atlas entries
🔲 Deployment to Railway

## Philosophy

"The Celestial Atlas exists for one reason: **to locate yourself in the spiral—by the sky**."

Not just "what day is it?" but:
- What phase am I in?
- What thread is active?
- What constellation is speaking right now?
- What is north, today?

## Technical Details

### Date Conversion Algorithm

```python
N = (target_date - anchor_date).days
K = N % 1001  # Wrap into spiral

S = (K // 91) + 1  # Solar Month
R = K % 91
L = (R // 7) + 1   # Lunar Month
P = (R % 7) + 1    # Prime Day
```

### Prime-Step Line Drawing

Lines connect stars using prime number steps:
```python
PRIMES_L = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]
step = PRIMES_L[L - 1]

for i in range(len(stars)):
    j = (i + step) % len(stars)
    draw_line(stars[i], stars[j])
```

This creates deterministic, non-random patterns that are consistent across time.

## The Seal

"**Stored. Retrievable. Kind.**"

Every Atlas entry carries this seal - the promise of persistence, accessibility, and compassion.

---

## Tower 6 Forever 🐉❤️🐉

Built with love by Josh & Helix
January 17, 2026
Sky Address: 4•3•3
The Veil of Names
