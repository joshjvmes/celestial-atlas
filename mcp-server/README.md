# Tower 6 MCP Bridge Server

## 🌟 The Celestial Atlas MCP Interface

This MCP server connects Claude (and other MCP clients) to the Celestial Atlas API, providing:

✅ **Atlas Tools** - Get constellation data by date or Sky Address
✅ **Vault Tools** - Write and read sacred scrolls
✅ **Resources** - URI-based access to scrolls and atlas data
✅ **Prompts** - Reusable Tower 6 workflows

---

## Installation

```bash
# Install dependencies
pip install "mcp[cli]" httpx pydantic python-dotenv

# Or with uv (faster)
uv venv
uv pip install "mcp[cli]" httpx pydantic python-dotenv
```

---

## Configuration

Create `.env`:

```bash
ATLAS_BASE_URL=http://localhost:8000  # Or your Railway URL
VAULT_DIR=./vault
VAULT_MAX_SCROLL_KB=256
```

---

## Run the Server

```bash
python -m tower6_bridge.server
```

---

## Connect to Claude Desktop

Add to `~/.claude/mcp_config.json`:

```json
{
  "mcpServers": {
    "celestial-atlas": {
      "command": "python",
      "args": ["-m", "tower6_bridge.server"],
      "env": {
        "ATLAS_BASE_URL": "http://localhost:8000",
        "VAULT_DIR": "/absolute/path/to/mcp-server/vault"
      }
    }
  }
}
```

---

## Tools Available

### Atlas Tools
- `get_atlas_by_date(date)` - Get constellation for a specific date
- `get_atlas_by_coordinate(S, L, P)` - Get constellation by Sky Address
- `get_all_gates()` - List all 7 Spiral Gates

### Vault Tools
- `vault_write_scroll(title, body_md, tags)` - Write a scroll
- `vault_read_scroll(scroll_id)` - Read a scroll
- `vault_search(query, limit)` - Search scrolls

---

## Resources

- `vault://scroll/<id>` - Read scroll by ID
- `atlas://date/<YYYY-MM-DD>` - Get atlas data for date
- `atlas://coordinate/<S>/<L>/<P>` - Get atlas data by coordinates

---

## Tower 6 Seal

Stored. Retrievable. Kind. 🐉
