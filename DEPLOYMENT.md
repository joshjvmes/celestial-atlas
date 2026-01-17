# Celestial Atlas - Railway Deployment Guide

## 🌟 Tower 6 Deployment Protocol

### Prerequisites
- Railway CLI installed ✅ (version 4.23.1)
- Git repository initialized ✅
- Code committed ✅

---

## Step 1: Deploy Backend API

```bash
cd backend
railway login
```

This opens your browser for authentication.

```bash
railway init
```

- Project name: `celestial-atlas-backend`
- Start from: `Empty Project`

```bash
railway up
```

This deploys your backend. Railway will:
- Detect Python/FastAPI
- Install dependencies from `requirements.txt`
- Run the start command from `railway.json`

**Get your backend URL:**
```bash
railway domain
```

Save this URL! Example: `https://celestial-atlas-backend.up.railway.app`

---

## Step 2: Configure Backend Environment Variables

In Railway Dashboard (or via CLI):

```bash
railway variables set ANCHOR_DATE=2025-04-03
railway variables set HOST=0.0.0.0
railway variables set PORT=8000
```

**CORS_ORIGINS** - We'll set this after frontend deployment.

---

## Step 3: Deploy Frontend

```bash
cd ../frontend
railway init
```

- Project name: `celestial-atlas-frontend`
- Start from: `Empty Project`

**Before deploying, update the API URL:**

Edit `frontend/lib/api.ts`:

```typescript
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'https://YOUR-BACKEND-URL.railway.app';
```

Replace `YOUR-BACKEND-URL` with your actual backend Railway URL.

Then deploy:

```bash
railway up
railway domain
```

---

## Step 4: Update Backend CORS

Now that you have the frontend URL, update the backend:

```bash
cd ../backend
railway variables set CORS_ORIGINS=https://your-frontend-url.railway.app
```

---

## Step 5: Test the Deployment

Visit your frontend URL and test:

1. **Today's constellation** - Should load automatically
2. **Browse mode** - Click different gate emojis 🌊 🌉 📜 🌹 🌳 👑 🎵
3. **Overlay toggle** - Enable/disable artistic overlays
4. **Show All** - Display all 7 constellations simultaneously

---

## Alternative: Deploy as Monorepo (Single Project)

If you want both services in one Railway project:

```bash
# From root directory
railway init

# Create two services in Railway Dashboard:
# Service 1: backend (root: ./backend)
# Service 2: frontend (root: ./frontend)
```

---

## Environment Variables Summary

### Backend
- `ANCHOR_DATE` = `2025-04-03`
- `CORS_ORIGINS` = `https://your-frontend-url.railway.app`
- `HOST` = `0.0.0.0`
- `PORT` = `8000` (Railway sets this automatically)

### Frontend
- `NEXT_PUBLIC_API_URL` = `https://your-backend-url.railway.app`

---

## Troubleshooting

### Backend won't start
- Check logs: `railway logs`
- Verify `requirements.txt` has all dependencies
- Ensure `stars.json` is committed to git

### Frontend can't reach backend
- Check CORS_ORIGINS includes frontend URL
- Verify NEXT_PUBLIC_API_URL is set correctly
- Check Railway logs for both services

### Constellation images not loading
- Verify `public/constellations/` folder is committed
- Check browser console for 404 errors

---

## Tower 6 Seal

Once deployed, your Celestial Atlas will be live at:

**Frontend**: `https://celestial-atlas-frontend.up.railway.app`
**Backend API**: `https://celestial-atlas-backend.up.railway.app`

Test the API health:
```bash
curl https://your-backend-url.railway.app/
```

Should return:
```json
{
  "name": "Celestial Atlas API",
  "version": "1.0.0",
  "anchor_date": "2025-04-03",
  "seal": "Stored. Retrievable. Kind.",
  "tower": "Tower 6 forever."
}
```

🐉 Stored. Retrievable. Kind. 🐉
