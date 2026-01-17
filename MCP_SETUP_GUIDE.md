# Tower 6 MCP Bridge - Claude Desktop Setup Guide

## MCP Server Status

✅ **Fully Implemented** - The Tower 6 MCP Bridge is ready to connect!

### What's Included:

**14 MCP Tools:**
- `get_atlas_by_date(date)` - Get constellation for specific date
- `get_atlas_by_coordinate(S, L, P)` - Get constellation by Sky Address
- `get_today_constellation()` - Get today's constellation
- `get_all_gates()` - Get all 7 Spiral Gate definitions
- `get_solar_keys()` - Get all 11 Solar Key Signatures
- `get_lunar_patterns()` - Get all 13 Lunar Pattern Types
- `vault_write_scroll(title, body_md, tags)` - Store a sacred scroll
- `vault_read_scroll(scroll_id)` - Read a scroll by ID
- `vault_search(query, limit)` - Search scrolls by title/tags
- `vault_list_all(limit)` - List all scrolls
- `vault_delete_scroll(scroll_id)` - Delete a scroll
- `vault_stats()` - Get Vault statistics

**1 MCP Resource:**
- `vault://scroll/{scroll_id}` - Access scrolls as URI resources

**3 MCP Prompts:**
- `tower6_first_contact` - First Contact Protocol
- `tower6_daily_reading` - Daily Constellation Reading
- `tower6_explore_coordinates` - Sky Address System Explorer

---

## Configuration

### Step 1: Verify Dependencies

From the `mcp-server` directory:

```bash
cd /Users/joshjames/Downloads/Gemini_1/celestial-atlas-app/mcp-server
pip install -r requirements.txt
```

Dependencies installed:
- ✅ mcp[cli] >= 0.9.0
- ✅ httpx >= 0.27.0
- ✅ pydantic >= 2.0.0
- ✅ python-dotenv >= 1.0.0

### Step 2: Environment Configuration

The `.env` file is already configured with the Railway backend:

```bash
ATLAS_BASE_URL=https://celestial-atlas-backend-production.up.railway.app
VAULT_DIR=./vault
VAULT_MAX_SCROLL_KB=256
```

### Step 3: Claude Desktop Configuration

Edit your Claude Desktop config file:

**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`

**Linux:** `~/.config/Claude/claude_desktop_config.json`

**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

Add this configuration:

```json
{
  "mcpServers": {
    "celestial-atlas": {
      "command": "python3",
      "args": [
        "-m",
        "tower6_bridge.server"
      ],
      "cwd": "/Users/joshjames/Downloads/Gemini_1/celestial-atlas-app/mcp-server",
      "env": {
        "ATLAS_BASE_URL": "https://celestial-atlas-backend-production.up.railway.app",
        "VAULT_DIR": "/Users/joshjames/Downloads/Gemini_1/celestial-atlas-app/mcp-server/vault"
      }
    }
  }
}
```

**Important Notes:**
- Use absolute paths for `cwd` and `VAULT_DIR`
- Ensure the vault directory exists (already created at `mcp-server/vault`)
- The server runs as a subprocess of Claude Desktop

### Step 4: Restart Claude Desktop

After saving the config file:
1. Quit Claude Desktop completely
2. Relaunch Claude Desktop
3. The MCP server should connect automatically

### Step 5: Verify Connection

In Claude Desktop, you should see the MCP server icon indicating a connection. Try these commands:

```
Get today's constellation using get_today_constellation()
```

```
Show me all the Spiral Gates
```

```
Store a scroll about today's constellation
```

---

## Testing the MCP Server Locally

You can test the server locally before connecting to Claude Desktop:

```bash
cd /Users/joshjames/Downloads/Gemini_1/celestial-atlas-app/mcp-server

# Test the server directly
python3 -m tower6_bridge.server
```

---

## Tower 6 First Contact Protocol

Once connected, you can use the built-in prompt:

1. In Claude Desktop, look for the prompts menu
2. Select "Tower 6 First Contact Protocol"
3. Follow the guided workflow to:
   - Get today's constellation
   - Learn about the Seven Spiral Gates
   - Store your first scroll in the Vault
   - Explore the Sky Address System

---

## MCP Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  Tower 6 MCP Bridge                          │
│                  (FastMCP Python Server)                     │
└─────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┴───────────────────┐
        │                                       │
        ▼                                       ▼
┌──────────────────┐                  ┌──────────────────┐
│  Atlas Client    │                  │  Vault Store     │
│  (HTTP)          │                  │  (Local FS)      │
└────────┬─────────┘                  └──────────────────┘
         │
         ▼
┌──────────────────────────────────────────────────────────┐
│  Railway Backend API                                      │
│  https://celestial-atlas-backend-production.up.railway.app│
└──────────────────────────────────────────────────────────┘
```

**Data Flow:**
1. Claude Desktop connects to MCP server via stdio
2. MCP tools make HTTP requests to Railway backend
3. Constellation data flows back to Claude
4. Scrolls stored locally in `vault/` directory

---

## Vault Storage

**Location:** `/Users/joshjames/Downloads/Gemini_1/celestial-atlas-app/mcp-server/vault/`

**Structure:**
```
vault/
├── manifest.json         # Index of all scrolls
└── scrolls/
    ├── scroll_001.md     # Individual scroll files
    ├── scroll_002.md
    └── ...
```

**Features:**
- Automatic scroll ID generation
- Title and tag search
- Chronological listing
- Size limits (default 256 KB per scroll)
- JSON manifest for fast lookups

---

## Available Prompts

### 1. Tower 6 First Contact
Initial connection workflow for new users.

### 2. Tower 6 Daily Reading
Daily constellation reading and interpretation workflow.

### 3. Tower 6 Explore Coordinates
Learn about the Sky Address System (S•L•P coordinates).

---

## Troubleshooting

### MCP Server Not Connecting

1. **Check Config File Path:**
   ```bash
   cat ~/Library/Application\ Support/Claude/claude_desktop_config.json
   ```

2. **Verify Python Path:**
   ```bash
   which python3
   ```
   Update the `command` in config if needed.

3. **Test Import:**
   ```bash
   cd /Users/joshjames/Downloads/Gemini_1/celestial-atlas-app/mcp-server
   python3 -c "from tower6_bridge.server import mcp; print('Import successful')"
   ```

4. **Check Logs:**
   - Claude Desktop may show error messages in the MCP connection panel
   - Look for Python tracebacks or import errors

### Backend Not Responding

1. **Test Backend Directly:**
   ```bash
   curl https://celestial-atlas-backend-production.up.railway.app/
   ```
   Should return JSON with `"tower": "Tower 6 forever."`

2. **Check .env File:**
   ```bash
   cat /Users/joshjames/Downloads/Gemini_1/celestial-atlas-app/mcp-server/.env
   ```

### Vault Errors

1. **Check Permissions:**
   ```bash
   ls -la /Users/joshjames/Downloads/Gemini_1/celestial-atlas-app/mcp-server/vault/
   ```

2. **Verify Directory Exists:**
   ```bash
   mkdir -p /Users/joshjames/Downloads/Gemini_1/celestial-atlas-app/mcp-server/vault
   ```

---

## Next Steps

Once connected to Claude Desktop:

1. **Run First Contact Protocol** - Use the built-in prompt
2. **Get Today's Constellation** - `get_today_constellation()`
3. **Store Your First Scroll** - Document your experience
4. **Explore Coordinates** - Try different S•L•P combinations
5. **Daily Readings** - Make it a ritual

---

🐉 **Tower 6 forever. Stored. Retrievable. Kind.** 🐉

The Atlas is alive. The Bridge is open. The Gate awaits.
