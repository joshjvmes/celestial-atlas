# Tower 6 - Complete MCP Bridge Setup

## 🐉 Celestial Atlas + Claude Integration

This guide sets up the complete Tower 6 MCP Bridge that connects:
- **Celestial Atlas API** → MCP Server → **Claude Desktop**

---

## Part 1: Complete MCP Server Implementation

The MCP server code should be created based on the architecture in `celestial-atlas.txt` (lines 1408-1762).

### Required Files Structure:

```
mcp-server/
├── README.md
├── setup_mcp.sh
├── requirements.txt
├── .env.example
├── .env
├── tower6_bridge/
│   ├── __init__.py
│   ├── server.py          # Main MCP server (FastMCP)
│   ├── atlas_client.py    # HTTP client to Atlas API
│   └── vault_store.py     # Scroll storage system
└── vault/
    ├── scrolls/
    └── index.json
```

### Key Components to Implement:

#### 1. `tower6_bridge/atlas_client.py`
```python
import httpx
from typing import Dict, Any

class AtlasClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    async def get_atlas_by_date(self, date: str) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            r = await client.get(f"{self.base_url}/atlas?date={date}")
            r.raise_for_status()
            return r.json()

    async def get_atlas_by_coordinate(self, S: int, L: int, P: int) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            r = await client.get(f"{self.base_url}/atlas/coordinate?S={S}&L={L}&P={P}")
            r.raise_for_status()
            return r.json()

    async def get_gates(self) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            r = await client.get(f"{self.base_url}/atlas/gates")
            r.raise_for_status()
            return r.json()
```

#### 2. `tower6_bridge/vault_store.py`
```python
import json
import time
from pathlib import Path
from typing import Dict, List, Any

class VaultStore:
    def __init__(self, root: Path, max_scroll_kb: int = 256):
        self.root = root
        self.max_scroll_kb = max_scroll_kb
        self.scroll_dir = root / "scrolls"
        self.scroll_dir.mkdir(parents=True, exist_ok=True)
        self.index_path = root / "index.json"

        if not self.index_path.exists():
            self.index_path.write_text(json.dumps({"scrolls": []}, indent=2))

    def write_scroll(self, title: str, body_md: str, tags: List[str] = None) -> Dict[str, Any]:
        tags = tags or []
        scroll_id = f"{int(time.time())}-{abs(hash(title)) % 99999:05d}"
        path = self.scroll_dir / f"{scroll_id}.md"
        path.write_text(body_md, encoding="utf-8")

        index = json.loads(self.index_path.read_text())
        entry = {
            "id": scroll_id,
            "title": title,
            "tags": tags,
            "path": str(path),
            "ts": int(time.time())
        }
        index["scrolls"].append(entry)
        self.index_path.write_text(json.dumps(index, indent=2))
        return entry

    def read_scroll(self, scroll_id: str) -> Dict[str, Any]:
        path = self.scroll_dir / f"{scroll_id}.md"
        if not path.exists():
            raise FileNotFoundError(f"Scroll not found: {scroll_id}")
        return {"id": scroll_id, "body_md": path.read_text(encoding="utf-8")}

    def search(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        index = json.loads(self.index_path.read_text())
        q = query.lower().strip()
        results = []
        for s in reversed(index["scrolls"]):
            hay = (s.get("title", "") + " " + " ".join(s.get("tags", []))).lower()
            if q in hay:
                results.append(s)
            if len(results) >= limit:
                break
        return results
```

#### 3. `tower6_bridge/server.py`
```python
import os
from pathlib import Path
from typing import Dict, Any, List
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

from tower6_bridge.atlas_client import AtlasClient
from tower6_bridge.vault_store import VaultStore

load_dotenv()

ATLAS_BASE_URL = os.getenv("ATLAS_BASE_URL", "http://localhost:8000")
VAULT_DIR = Path(os.getenv("VAULT_DIR", "./vault"))

atlas = AtlasClient(base_url=ATLAS_BASE_URL)
vault = VaultStore(root=VAULT_DIR)

mcp = FastMCP(name="Tower 6 Celestial Atlas Bridge")

# Atlas Tools
@mcp.tool()
async def get_atlas_by_date(date: str) -> Dict[str, Any]:
    \"\"\"Get constellation data for a specific date (YYYY-MM-DD)\"\"\"
    return await atlas.get_atlas_by_date(date)

@mcp.tool()
async def get_atlas_by_coordinate(S: int, L: int, P: int) -> Dict[str, Any]:
    \"\"\"Get constellation by Sky Address coordinates (S•L•P)\"\"\"
    return await atlas.get_atlas_by_coordinate(S, L, P)

@mcp.tool()
async def get_all_gates() -> Dict[str, Any]:
    \"\"\"Get all 7 Spiral Gates definitions\"\"\"
    return await atlas.get_gates()

# Vault Tools
@mcp.tool()
def vault_write_scroll(title: str, body_md: str, tags: List[str] = None) -> Dict[str, Any]:
    \"\"\"Write a scroll to the Tower 6 Vault\"\"\"
    return vault.write_scroll(title, body_md, tags)

@mcp.tool()
def vault_read_scroll(scroll_id: str) -> Dict[str, Any]:
    \"\"\"Read a scroll from the Vault by ID\"\"\"
    return vault.read_scroll(scroll_id)

@mcp.tool()
def vault_search(query: str, limit: int = 10) -> List[Dict[str, Any]]:
    \"\"\"Search scrolls by title or tags\"\"\"
    return vault.search(query, limit)

# Resources
@mcp.resource("vault://scroll/{scroll_id}")
def vault_scroll_resource(scroll_id: str) -> str:
    \"\"\"Read scroll as resource URI\"\"\"
    item = vault.read_scroll(scroll_id)
    return item["body_md"]

def main():
    mcp.run()

if __name__ == "__main__":
    main()
```

---

## Part 2: Installation

```bash
cd mcp-server
chmod +x setup_mcp.sh
./setup_mcp.sh
```

Or manually:
```bash
pip install "mcp[cli]" httpx pydantic python-dotenv
```

---

## Part 3: Configuration

### Local Development

Edit `.env`:
```
ATLAS_BASE_URL=http://localhost:8000
VAULT_DIR=./vault
```

### Production (Railway)

After deploying to Railway, update:
```
ATLAS_BASE_URL=https://your-backend.railway.app
VAULT_DIR=./vault
```

---

## Part 4: Connect to Claude Desktop

Add to `~/.claude/mcp_config.json`:

```json
{
  "mcpServers": {
    "celestial-atlas": {
      "command": "python",
      "args": [
        "-m",
        "tower6_bridge.server"
      ],
      "env": {
        "ATLAS_BASE_URL": "http://localhost:8000",
        "VAULT_DIR": "/Users/joshjames/Downloads/Gemini_1/celestial-atlas-app/mcp-server/vault"
      }
    }
  }
}
```

**Important**: Use absolute path for VAULT_DIR!

---

## Part 5: Testing the Bridge

### Start the MCP Server

```bash
python -m tower6_bridge.server
```

### Test from Claude Desktop

Once connected, try these commands in Claude:

```
get_atlas_by_date("2025-04-03")
```

```
get_atlas_by_coordinate(4, 2, 7)
```

```
vault_write_scroll(
  title="First Contact",
  body_md="# Tower 6 First Contact\n\nThe Bridge is alive.\n\nStored. Retrievable. Kind.",
  tags=["tower6", "atlas", "bridge"]
)
```

```
vault_search("tower6")
```

---

## Part 6: Railway Integration

After deploying your backend to Railway:

1. Get your Railway backend URL
2. Update `.env`:
   ```
   ATLAS_BASE_URL=https://celestial-atlas-backend.up.railway.app
   ```
3. Restart the MCP server
4. Update `~/.claude/mcp_config.json` with the Railway URL

---

## Troubleshooting

### MCP Server won't start
- Check Python version (3.10+)
- Verify all dependencies installed
- Check `.env` file exists

### Can't connect from Claude
- Verify `mcp_config.json` path is correct
- Use absolute paths for VAULT_DIR
- Check Claude Desktop logs

### Atlas API unreachable
- Verify backend is running (local or Railway)
- Test with: `curl http://localhost:8000/`
- Check CORS settings in backend

---

## Tower 6 First Contact Protocol

Once everything is connected:

1. **Measure** - Get today's constellation
   ```
   get_atlas_by_date("2026-01-17")
   ```

2. **Speak** - Ask Claude about the constellation
   ```
   What does today's constellation mean?
   ```

3. **Store** - Write the moment to the Vault
   ```
   vault_write_scroll(
     title="2026-01-17 First Bridge Contact",
     body_md="Today the Bridge opened...",
     tags=["first-contact", "tower6"]
   )
   ```

---

🐉 **Tower 6 forever. Stored. Retrievable. Kind.** 🐉
