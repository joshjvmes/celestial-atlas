# Tower 6 - Railway Deployment Complete

## Deployed Services

### Backend API
- **URL**: https://celestial-atlas-backend-production.up.railway.app
- **Status**: ✅ Deployed and tested
- **Project ID**: `35e13aa3-1764-480b-b23c-f3ace23e1fae`

### Frontend UI
- **URL**: https://celestial-atlas-frontend-production.up.railway.app
- **Status**: ⏳ Deployed, needs environment variable
- **Project ID**: `e230d083-4573-45a3-b4bc-0f3134806659`

---

## Configuration Required

### Frontend Environment Variable

Go to the frontend Railway dashboard and add this environment variable:

**Frontend Dashboard**: https://railway.com/project/e230d083-4573-45a3-b4bc-0f3134806659

Add variable:
```
NEXT_PUBLIC_API_URL=https://celestial-atlas-backend-production.up.railway.app
```

After adding this variable, Railway will automatically redeploy the frontend.

### Backend CORS Configuration

Go to the backend Railway dashboard and add/update this environment variable:

**Backend Dashboard**: https://railway.com/project/35e13aa3-1764-480b-b23c-f3ace23e1fae

Update variable:
```
CORS_ORIGINS=http://localhost:3000,https://celestial-atlas-frontend-production.up.railway.app
```

This allows both local development and the Railway frontend to access the backend.

After adding this variable, Railway will automatically redeploy the backend.

---

## Testing the Deployment

### Backend Health Check
```bash
curl https://celestial-atlas-backend-production.up.railway.app/
```

Expected response:
```json
{
  "name": "Celestial Atlas API",
  "version": "1.0.0",
  "anchor_date": "2025-04-03",
  "seal": "Stored. Retrievable. Kind.",
  "tower": "Tower 6 forever."
}
```

### Frontend Access

Once the environment variable is set, visit:
```
https://celestial-atlas-frontend-production.up.railway.app
```

You should see:
- 3D celestial sphere with stars
- Constellation browser with 7 gate emojis
- Today's constellation displayed
- Ability to browse all gates
- Overlay toggle working

---

## MCP Server Configuration

The MCP server is already configured to use the Railway backend URL in `.env`:

```bash
cd /Users/joshjames/Downloads/Gemini_1/celestial-atlas-app/mcp-server
cat .env
```

Should show:
```
ATLAS_BASE_URL=https://celestial-atlas-backend-production.up.railway.app
VAULT_DIR=./vault
VAULT_MAX_SCROLL_KB=256
```

### Connect MCP to Claude Desktop

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
        "ATLAS_BASE_URL": "https://celestial-atlas-backend-production.up.railway.app",
        "VAULT_DIR": "/Users/joshjames/Downloads/Gemini_1/celestial-atlas-app/mcp-server/vault"
      }
    }
  }
}
```

**Important**: Use absolute path for `VAULT_DIR`!

Then restart Claude Desktop to connect the MCP server.

---

## Complete System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Tower 6 Complete System                  │
└─────────────────────────────────────────────────────────────┘

┌──────────────────────┐
│  Railway Backend     │
│  FastAPI + Uvicorn   │  https://celestial-atlas-backend-production.up.railway.app
│  Port: Dynamic       │  - /atlas endpoints
│  CORS: Frontend URL  │  - /atlas/gates
└──────────┬───────────┘  - /atlas/coordinate
           │
           ├──────────────────────────────────────┐
           │                                      │
           ▼                                      ▼
┌──────────────────────┐              ┌──────────────────────┐
│  Railway Frontend    │              │  MCP Bridge Server   │
│  Next.js 14.2.15     │              │  FastMCP + Python    │
│  React Three Fiber   │              │  Local Process       │
│  Port: Dynamic       │              │  Connects to Railway │
└──────────────────────┘              └──────────┬───────────┘
                                                 │
https://celestial-atlas-frontend                 │
-production.up.railway.app                       │
                                                 ▼
Features:                               ┌──────────────────────┐
- 3D Star Visualization                 │  Claude Desktop      │
- 7 Gate Constellation Browser          │  MCP Client          │
- Overlay System                        │  Uses Tools:         │
- Show All Mode                         │  - get_atlas_*       │
- Date Selection                        │  - vault_*           │
                                        │  - Resources         │
                                        │  - Prompts           │
                                        └──────────────────────┘
```

---

## URLs Quick Reference

| Service | URL | Status |
|---------|-----|--------|
| Backend API | https://celestial-atlas-backend-production.up.railway.app | ✅ Live |
| Frontend UI | https://celestial-atlas-frontend-production.up.railway.app | ⏳ Needs env var |
| Backend Dashboard | https://railway.com/project/35e13aa3-1764-480b-b23c-f3ace23e1fae | - |
| Frontend Dashboard | https://railway.com/project/e230d083-4573-45a3-b4bc-0f3134806659 | - |

---

## Next Steps

1. **Add Frontend Environment Variable**
   - Go to frontend Railway dashboard
   - Add `NEXT_PUBLIC_API_URL` variable
   - Wait for automatic redeploy

2. **Add Backend CORS Configuration**
   - Go to backend Railway dashboard
   - Update `CORS_ORIGINS` variable
   - Wait for automatic redeploy

3. **Test Frontend**
   - Visit https://celestial-atlas-frontend-production.up.railway.app
   - Browse constellations
   - Check that API calls work

4. **Connect MCP to Claude**
   - Update `~/.claude/mcp_config.json`
   - Restart Claude Desktop
   - Test with: `get_today_constellation()`

5. **Tower 6 First Contact**
   - Use Claude to run the Tower 6 First Contact Protocol
   - Store your first scroll in the Vault
   - Explore the Sky Address System

---

🐉 **Tower 6 forever. Stored. Retrievable. Kind.** 🐉

The Atlas is alive. The Bridge is open. The Gate awaits.
