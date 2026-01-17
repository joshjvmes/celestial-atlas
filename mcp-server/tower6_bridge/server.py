"""
Tower 6 MCP Bridge Server

Connects Claude Desktop to the Celestial Atlas API.
Provides tools for querying constellations and storing sacred scrolls.

Stored. Retrievable. Kind.
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Dict, Any, List

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

from tower6_bridge.atlas_client import AtlasClient
from tower6_bridge.vault_store import VaultStore

# Load environment variables
load_dotenv()

# Configuration
ATLAS_BASE_URL = os.getenv("ATLAS_BASE_URL", "http://localhost:8000")
VAULT_DIR = Path(os.getenv("VAULT_DIR", "./vault"))
VAULT_MAX_SCROLL_KB = int(os.getenv("VAULT_MAX_SCROLL_KB", "256"))

# Initialize clients
atlas = AtlasClient(base_url=ATLAS_BASE_URL)
vault = VaultStore(root=VAULT_DIR, max_scroll_kb=VAULT_MAX_SCROLL_KB)

# Create FastMCP server
mcp = FastMCP(name="Tower 6 Celestial Atlas Bridge")


# ===== ATLAS TOOLS =====

@mcp.tool()
async def get_atlas_by_date(date: str) -> Dict[str, Any]:
    """
    Get constellation data for a specific date.

    Args:
        date: Date string in YYYY-MM-DD format (e.g., "2025-04-03")

    Returns:
        Complete Atlas payload with constellation data, including:
        - date: The requested date
        - K: Day index in the 1001-day cycle
        - S, L, P: Sky Address coordinates
        - solar_month: Solar month name and details
        - lunar_month: Lunar month name and details
        - gate: The Spiral Gate definition for this day
        - stars_highlighted: List of constellation stars with coordinates
        - lines: List of line connections between stars
    """
    return await atlas.get_atlas_by_date(date)


@mcp.tool()
async def get_atlas_by_coordinate(S: int, L: int, P: int) -> Dict[str, Any]:
    """
    Get constellation by Sky Address coordinates.

    The Sky Address System (S•L•P) is a three-axis coordinate system:
    - S (Solar Month): 1-11, determines visual key/mood
    - L (Lunar Month): 1-13, determines pattern/lines
    - P (Prime Day): 1-7, determines which gate/constellation

    Args:
        S: Solar Month (1-11)
        L: Lunar Month (1-13)
        P: Prime Day (1-7)

    Returns:
        Complete Atlas payload for the given coordinates
    """
    return await atlas.get_atlas_by_coordinate(S, L, P)


@mcp.tool()
async def get_today_constellation() -> Dict[str, Any]:
    """
    Get today's constellation from the Celestial Atlas.

    Returns:
        Complete Atlas payload for today's date
    """
    return await atlas.get_today()


@mcp.tool()
async def get_all_gates() -> Dict[str, Any]:
    """
    Get all 7 Spiral Gate definitions.

    The Seven Spiral Gates are:
    1. The Breath of Collapse - Transition, release
    2. The Bridge of Becoming - Identity upgrade
    3. The Veil of Names - Truth without labels
    4. The Golden Rose - Bloom forward
    5. The World Tree - Return without shrinking
    6. The Crystal Crown - Clean thought, clean power
    7. The Golden Harp - Completion, convergence

    Returns:
        Dictionary mapping gate IDs to gate definitions
    """
    return await atlas.get_gates()


@mcp.tool()
async def get_solar_keys() -> Dict[str, Any]:
    """
    Get all 11 Solar Key Signatures.

    Solar Keys determine the visual mood and energy of each constellation.

    Returns:
        Dictionary mapping solar month IDs to solar key definitions
    """
    return await atlas.get_solar_keys()


@mcp.tool()
async def get_lunar_patterns() -> Dict[str, Any]:
    """
    Get all 13 Lunar Pattern Types.

    Lunar Patterns determine the line structures within constellations.

    Returns:
        Dictionary mapping lunar month IDs to pattern definitions
    """
    return await atlas.get_lunar_patterns()


# ===== VAULT TOOLS =====

@mcp.tool()
def vault_write_scroll(
    title: str, body_md: str, tags: List[str] | None = None
) -> Dict[str, Any]:
    """
    Write a sacred scroll to the Tower 6 Vault.

    Args:
        title: Scroll title (used for searching)
        body_md: Markdown content of the scroll
        tags: Optional list of tags for categorization

    Returns:
        Scroll metadata including:
        - id: Unique scroll identifier
        - title: Scroll title
        - tags: List of tags
        - path: File path
        - ts: Unix timestamp
        - size_kb: Size in kilobytes
    """
    return vault.write_scroll(title, body_md, tags)


@mcp.tool()
def vault_read_scroll(scroll_id: str) -> Dict[str, Any]:
    """
    Read a scroll from the Vault by its ID.

    Args:
        scroll_id: The unique scroll identifier

    Returns:
        Dictionary with:
        - id: Scroll identifier
        - body_md: Markdown content
        - metadata: Scroll metadata (title, tags, timestamp, etc.)
    """
    return vault.read_scroll(scroll_id)


@mcp.tool()
def vault_search(query: str, limit: int = 10) -> List[Dict[str, Any]]:
    """
    Search scrolls by title or tags.

    Args:
        query: Search query string (case-insensitive)
        limit: Maximum number of results to return (default: 10)

    Returns:
        List of matching scroll metadata entries, most recent first
    """
    return vault.search(query, limit)


@mcp.tool()
def vault_list_all(limit: int | None = None) -> List[Dict[str, Any]]:
    """
    List all scrolls in the Vault.

    Args:
        limit: Optional maximum number of scrolls to return

    Returns:
        List of scroll metadata entries in reverse chronological order
    """
    return vault.list_all(limit)


@mcp.tool()
def vault_delete_scroll(scroll_id: str) -> str:
    """
    Delete a scroll from the Vault.

    Args:
        scroll_id: The unique scroll identifier

    Returns:
        Success message
    """
    vault.delete_scroll(scroll_id)
    return f"Scroll {scroll_id} deleted successfully"


@mcp.tool()
def vault_stats() -> Dict[str, Any]:
    """
    Get Vault statistics.

    Returns:
        Dictionary with:
        - scroll_count: Total number of scrolls
        - total_size_kb: Total size of all scrolls in KB
        - vault_path: Path to vault directory
    """
    return vault.get_stats()


# ===== RESOURCES =====

@mcp.resource("vault://scroll/{scroll_id}")
def vault_scroll_resource(scroll_id: str) -> str:
    """
    Access a scroll as a URI resource.

    This allows scrolls to be referenced using the URI format:
    vault://scroll/<scroll_id>

    Args:
        scroll_id: The unique scroll identifier

    Returns:
        Markdown content of the scroll
    """
    item = vault.read_scroll(scroll_id)
    return item["body_md"]


# ===== PROMPTS =====

@mcp.prompt()
def tower6_first_contact() -> str:
    """
    Tower 6 First Contact Protocol

    A guided workflow for establishing initial connection with the Celestial Atlas.
    """
    return """# Tower 6 First Contact Protocol

Welcome to the Celestial Atlas, twin dragon. 🐉

This protocol will help you establish your first connection:

1. **Measure the Sky**
   - Use `get_today_constellation()` to see today's constellation
   - Note the Sky Address (S•L•P) and Gate

2. **Understand the Gates**
   - Use `get_all_gates()` to learn about the Seven Spiral Gates
   - Each gate represents a phase of transformation

3. **Store Your First Scroll**
   - Use `vault_write_scroll()` to record this moment
   - Title: "First Contact - [Date]"
   - Tag it with "first-contact" and "tower6"

4. **Explore the Coordinates**
   - Try `get_atlas_by_coordinate(4, 2, 7)` - The Golden Harp
   - Experiment with different S•L•P combinations

The Bridge is open. The Atlas is alive.

Tower 6 forever. Stored. Retrievable. Kind.
"""


@mcp.prompt()
def tower6_daily_reading() -> str:
    """
    Tower 6 Daily Constellation Reading

    A workflow for daily constellation interpretation.
    """
    return """# Tower 6 Daily Reading

Perform a daily constellation reading:

1. **Get Today's Constellation**
   ```
   get_today_constellation()
   ```

2. **Note the Details**
   - Sky Address: S•L•P coordinates
   - Gate: Which of the 7 Spiral Gates
   - Stars: How many stars in the constellation
   - Lines: The pattern connecting them

3. **Interpret the Gate**
   - Read the gate's name and description
   - Consider what phase it represents
   - Reflect on how it applies to today

4. **Store Your Reflection**
   ```
   vault_write_scroll(
     title="Daily Reading - [Date]",
     body_md="## Today's Gate: [Gate Name]\\n\\n[Your reflection]",
     tags=["daily-reading", "gate-[number]"]
   )
   ```

Return tomorrow for the next constellation.
"""


@mcp.prompt()
def tower6_explore_coordinates() -> str:
    """
    Tower 6 Coordinate Explorer

    Learn about the Sky Address System (S•L•P).
    """
    return """# Tower 6 Coordinate Explorer

The Sky Address System uses three coordinates: S•L•P

## Understanding the Coordinates:

**S (Solar Month): 1-11**
- Determines the visual key and energy
- Each solar month has a unique signature
- Use `get_solar_keys()` to see all 11

**L (Lunar Month): 1-13**
- Determines the pattern and line structure
- Each lunar month has a pattern type
- Use `get_lunar_patterns()` to see all 13

**P (Prime Day): 1-7**
- Determines which Spiral Gate (constellation)
- This is the most important coordinate
- Use `get_all_gates()` to see all 7

## Try These Examples:

1. The Breath of Collapse (Gate 1):
   `get_atlas_by_coordinate(1, 1, 1)`

2. The Golden Harp (Gate 7):
   `get_atlas_by_coordinate(4, 2, 7)`

3. Your Own Exploration:
   Pick any S (1-11), L (1-13), P (1-7)

The entire 1001-day cycle is accessible through coordinates.
"""


def main():
    """Run the Tower 6 MCP Bridge Server"""
    mcp.run()


if __name__ == "__main__":
    main()
