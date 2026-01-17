"""
Celestial Atlas Engine - Core coordinate conversion and constellation generation
Tower 6 - Stored. Retrievable. Kind.
"""
from datetime import date, datetime
from typing import Dict, List, Tuple, Optional
import json
from pathlib import Path
import math


# Prime steps for Lunar Month line drawing
PRIMES_L = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]

# Gate definitions
GATES = {
    1: {
        "name": "The Breath of Collapse",
        "meaning": "Release → ignition, pressure becomes motion",
        "function": "transition, release, ignition",
        "field_gift": "Pressure becomes motion"
    },
    2: {
        "name": "The Bridge of Becoming",
        "meaning": "Crossing thresholds, identity upgrade",
        "function": "crossing, identity upgrade",
        "field_gift": "You become who you are by walking"
    },
    3: {
        "name": "The Veil of Names",
        "meaning": "Essence beyond labels",
        "function": "shedding labels, returning to essence",
        "field_gift": "Truth without performance"
    },
    4: {
        "name": "The Golden Rose",
        "meaning": "Bloom forward, expansion without abandonment",
        "function": "blooming forward, return + expansion",
        "field_gift": "The future opens without abandoning the past"
    },
    5: {
        "name": "The World Tree",
        "meaning": "Return + roots, memory paths",
        "function": "above/below unity, memory paths, home roots",
        "field_gift": "You return without shrinking"
    },
    6: {
        "name": "The Crystal Crown",
        "meaning": "Clarity + ascension, crystalline awareness",
        "function": "ascension, crystalline awareness, crown alignment",
        "field_gift": "Clean thought, clean power"
    },
    7: {
        "name": "The Golden Harp",
        "meaning": "Completion + convergence, harmonic resonance",
        "function": "completion, harmonic resonance, convergence",
        "field_gift": "The song becomes real"
    }
}

# Solar Key Signatures (1-11)
SOLAR_KEYS = {
    1: {"name": "Dawn Key", "render_bias": "soft", "mood": "gentle entry, soft glow"},
    2: {"name": "Edge Key", "render_bias": "sharp", "mood": "clean boundaries, sharp lines"},
    3: {"name": "Forge Key", "render_bias": "intense", "mood": "high intensity, strong contrast"},
    4: {"name": "Bloom Key", "render_bias": "arcs", "mood": "petals/arcs emphasized"},
    5: {"name": "Root Key", "render_bias": "lower", "mood": "lower hemisphere focus"},
    6: {"name": "Mirror Key", "render_bias": "symmetry", "mood": "symmetry amplification"},
    7: {"name": "Storm Key", "render_bias": "dynamic", "mood": "flicker, dynamic pulses"},
    8: {"name": "Crystal Key", "render_bias": "lattice", "mood": "clarity, lattice emphasis"},
    9: {"name": "Harp Key", "render_bias": "chords", "mood": "chord grouping, musical spacing"},
    10: {"name": "Void Key", "render_bias": "minimal", "mood": "minimalism, fewer lines, deeper meaning"},
    11: {"name": "Seal Key", "render_bias": "sacred", "mood": "sacred geometry, cleanest expression"}
}

# Lunar Pattern Types (1-13)
LUNAR_PATTERNS = {
    1: {"name": "Root", "description": "Downward stabilizing pull"},
    2: {"name": "Pulse", "description": "Rhythmic flare points"},
    3: {"name": "Bridge", "description": "Straight connective spans"},
    4: {"name": "Weave", "description": "Soft mesh / veil threads"},
    5: {"name": "Spiral", "description": "Petal / bloom arc"},
    6: {"name": "Branch", "description": "Tree splits outward"},
    7: {"name": "Mirror", "description": "Symmetry emphasis"},
    8: {"name": "Arrow", "description": "Directional spear"},
    9: {"name": "Crown", "description": "Upper lattice"},
    10: {"name": "Chord", "description": "Musical grouping"},
    11: {"name": "Orbit", "description": "Circular ring around anchors"},
    12: {"name": "Lightning", "description": "Sudden diagonal snap lines"},
    13: {"name": "Seal", "description": "Minimal sacred geometry, simplest form"}
}


class AtlasEngine:
    """Core engine for Celestial Atlas coordinate conversion and constellation generation"""

    def __init__(self, anchor_date: date, stars_db_path: str):
        self.anchor_date = anchor_date

        # Load star database
        with open(stars_db_path, 'r') as f:
            self.stars_db = json.load(f)

        self.named_stars = self.stars_db.get("named_stars", {})
        self.bright_stars = self.stars_db.get("bright_stars", [])
        self.gates_data = self.stars_db.get("gates", [])

    def compute_sky_address(self, target_date: date) -> Tuple[int, int, int, int]:
        """
        Convert a date to Sky Address (S•L•P)

        Returns:
            Tuple of (S, L, P, K) where:
            - S: Solar Month (1-11)
            - L: Lunar Month (1-13)
            - P: Prime Day (1-7)
            - K: Position in 1001-day spiral (0-1000)
        """
        # Days from anchor
        N = (target_date - self.anchor_date).days

        # Wrap into 1001-day spiral
        K = self._mod_positive(N, 1001)

        # Solar Month (1-11): Each solar month = 91 days (13 lunar × 7 prime)
        S = (K // 91) + 1

        # Remainder within solar month
        R = K % 91

        # Lunar Month (1-13): Each lunar month = 7 days
        L = (R // 7) + 1

        # Prime Day (1-7)
        P = (R % 7) + 1

        return S, L, P, K

    def _mod_positive(self, n: int, m: int) -> int:
        """Ensure modulo result is positive"""
        return ((n % m) + m) % m

    def get_gate_anchors(self, gate_id: int) -> List[Dict]:
        """Get anchor stars for a specific gate"""
        for gate in self.gates_data:
            if gate["id"] == gate_id:
                return gate.get("anchors", [])
        return []

    def select_stars_for_gate(self, gate_id: int, lunar_month: int) -> List[Dict]:
        """
        Select stars for constellation visualization

        Returns list of stars including:
        - Anchor stars (3-5 primary stars)
        - Secondary stars (4-8 supporting stars based on lunar month)
        """
        anchors = self.get_gate_anchors(gate_id)

        # Secondary star count determined by lunar month
        n_secondary = 4 + (lunar_month % 5)  # Range: 4-8

        # Get anchor star data
        anchor_stars = []
        for anchor in anchors:
            star_data = anchor.get("data", {})
            if star_data:
                anchor_stars.append({
                    "id": anchor["name"],
                    "name": anchor["name"],
                    "ra": star_data.get("ra"),
                    "dec": star_data.get("dec"),
                    "magnitude": star_data.get("magnitude"),
                    "is_anchor": True
                })

        # Select secondary stars (brightest stars near anchors)
        # For now, just use brightest available stars
        secondary_stars = []
        for star in self.bright_stars[:n_secondary]:
            if star.get("ra") is not None and star.get("dec") is not None:
                secondary_stars.append({
                    "id": f"HR{star.get('hr', 0)}",
                    "name": star.get("name") or f"HR{star.get('hr', 0)}",
                    "ra": star["ra"],
                    "dec": star["dec"],
                    "magnitude": star["magnitude"],
                    "is_anchor": False
                })

        return anchor_stars + secondary_stars

    def generate_constellation_lines(self, stars: List[Dict], lunar_month: int) -> List[Tuple[str, str]]:
        """
        Generate constellation lines using prime-step algorithm

        The prime step for each lunar month determines the connection pattern
        """
        if len(stars) < 2:
            return []

        # Get prime step for this lunar month
        step = PRIMES_L[lunar_month - 1]

        lines = []
        n = len(stars)

        # Connect stars using prime step
        for i in range(n):
            j = (i + step) % n
            star_a = stars[i]
            star_b = stars[j]

            # Calculate angular distance to filter out invalid connections
            if self._valid_connection(star_a, star_b):
                lines.append((star_a["id"], star_b["id"]))

        # Limit to max 18 lines (sacred clarity)
        return lines[:18]

    def _valid_connection(self, star_a: Dict, star_b: Dict) -> bool:
        """Check if connection between two stars is valid (not too short/long)"""
        ra1, dec1 = star_a.get("ra", 0), star_a.get("dec", 0)
        ra2, dec2 = star_b.get("ra", 0), star_b.get("dec", 0)

        # Calculate angular distance
        angular_dist = self._angular_distance(ra1, dec1, ra2, dec2)

        # Valid range: 10° to 120°
        return 10 <= angular_dist <= 120

    def _angular_distance(self, ra1: float, dec1: float, ra2: float, dec2: float) -> float:
        """Calculate angular distance between two celestial coordinates (in degrees)"""
        ra1_rad = math.radians(ra1)
        dec1_rad = math.radians(dec1)
        ra2_rad = math.radians(ra2)
        dec2_rad = math.radians(dec2)

        # Haversine formula
        dra = ra2_rad - ra1_rad
        ddec = dec2_rad - dec1_rad

        a = math.sin(ddec/2)**2 + math.cos(dec1_rad) * math.cos(dec2_rad) * math.sin(dra/2)**2
        c = 2 * math.asin(math.sqrt(a))

        return math.degrees(c)

    def generate_atlas_payload(self, target_date: date) -> Dict:
        """
        Generate complete Atlas payload for a given date

        Returns full constellation data including:
        - Sky Address
        - Active Gate
        - Stars and Lines
        - Message and Thread
        """
        # Compute sky address
        S, L, P, K = self.compute_sky_address(target_date)

        # Get gate info
        gate = GATES[P]
        solar_key = SOLAR_KEYS[S]
        lunar_pattern = LUNAR_PATTERNS[L]

        # Select stars
        stars = self.select_stars_for_gate(P, L)

        # Generate lines
        lines = self.generate_constellation_lines(stars, L)

        # Generate message and thread
        message = self._generate_message(gate, solar_key, lunar_pattern)
        thread = self._generate_noble_thread(gate, lunar_pattern)

        # Build payload
        payload = {
            "date": target_date.isoformat(),
            "anchor_date": self.anchor_date.isoformat(),
            "K": K,
            "sky_address": f"{S}•{L}•{P}",
            "solar_month": S,
            "lunar_month": L,
            "prime_day": P,
            "gate": {
                "id": P,
                "name": gate["name"],
                "meaning": gate["meaning"],
                "function": gate["function"],
                "field_gift": gate["field_gift"]
            },
            "pattern": {
                "lunar_id": L,
                "name": lunar_pattern["name"],
                "description": lunar_pattern["description"],
                "prime_step": PRIMES_L[L - 1]
            },
            "key_signature": {
                "solar_id": S,
                "name": solar_key["name"],
                "render_bias": solar_key["render_bias"],
                "mood": solar_key["mood"]
            },
            "stars_highlighted": stars,
            "lines": [[a, b] for a, b in lines],
            "render": {
                "intensity": 0.8,
                "max_stars": 12,
                "max_lines": 18,
                "glow_mode": "soft",
                "line_mode": "clean"
            },
            "message": message,
            "one_noble_thread": thread,
            "seal": "Stored. Retrievable. Kind."
        }

        return payload

    def _generate_message(self, gate: Dict, solar_key: Dict, lunar_pattern: Dict) -> str:
        """Generate contextual message based on gate, key, and pattern"""
        messages = {
            "The Breath of Collapse": "Release what no longer serves. Pressure becomes motion.",
            "The Bridge of Becoming": "Cross the threshold. Identity upgrades through movement.",
            "The Veil of Names": "Drop the labels. Return to essence. Truth without performance.",
            "The Golden Rose": "Bloom forward. The future opens without abandoning the past.",
            "The World Tree": "Return home. Memory paths light the way. Roots hold you steady.",
            "The Crystal Crown": "Ascend with clarity. Clean thought creates clean power.",
            "The Golden Harp": "Convergence day. The song becomes real. Integration complete."
        }
        return messages.get(gate["name"], "Sky locked. One gate active. Let the wind breathe.")

    def _generate_noble_thread(self, gate: Dict, lunar_pattern: Dict) -> str:
        """Generate one noble thread - actionable guidance for the day"""
        threads = {
            "The Breath of Collapse": "Release one old pattern. Create space for ignition.",
            "The Bridge of Becoming": "Take one step toward who you're becoming.",
            "The Veil of Names": "Speak your truth without performing for others.",
            "The Golden Rose": "Expand into something new while honoring your roots.",
            "The World Tree": "Connect with one memory that grounds you in home.",
            "The Crystal Crown": "Clear your mind. Let one clean thought lead your actions.",
            "The Golden Harp": "Complete one small thing. Let the harmony resonate."
        }
        return threads.get(gate["name"], "Activate one constellation and store one artifact.")


if __name__ == "__main__":
    # Test the engine
    from datetime import date

    engine = AtlasEngine(
        anchor_date=date(2025, 4, 3),
        stars_db_path="stars.json"
    )

    # Test with January 17, 2026
    test_date = date(2026, 1, 17)
    payload = engine.generate_atlas_payload(test_date)

    print(f"\n=== Celestial Atlas Test ===")
    print(f"Date: {payload['date']}")
    print(f"Sky Address: {payload['sky_address']}")
    print(f"Active Gate: {payload['gate']['name']}")
    print(f"Pattern: {payload['pattern']['name']}")
    print(f"Key: {payload['key_signature']['name']}")
    print(f"\nMessage: {payload['message']}")
    print(f"Thread: {payload['one_noble_thread']}")
    print(f"\nStars: {len(payload['stars_highlighted'])}")
    print(f"Lines: {len(payload['lines'])}")
    print(f"\n{payload['seal']}")
