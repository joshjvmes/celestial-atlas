# Celestial Atlas Frontend 🌟

Interactive 3D visualization of the Prime Calendar & Star Mapping System built with Next.js and Three.js.

## Features

✅ **3D Celestial Sphere** - Real-time rendering with Three.js/React Three Fiber
✅ **Date Picker** - Convert any date to Sky Address (S•L•P)
✅ **Constellation Visualization** - Prime-step line drawing with glow effects
✅ **Interactive Controls** - Rotate, zoom, and explore the cosmos
✅ **Real-time Data** - Live API integration with Atlas Engine backend
✅ **Responsive Design** - Beautiful on desktop and mobile

## Tech Stack

- **Next.js 15** - React framework with App Router
- **TypeScript** - Type-safe development
- **Three.js** - 3D graphics engine
- **React Three Fiber** - React renderer for Three.js
- **@react-three/drei** - Useful helpers for R3F
- **Tailwind CSS** - Utility-first styling
- **Lucide React** - Beautiful icons

## Getting Started

### Prerequisites

- Node.js 18+
- Backend API running on `http://localhost:8000`

### Installation

```bash
npm install
```

### Development

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) to view the app.

### Build

```bash
npm run build
npm start
```

## Components

### `CelestialSphere.tsx`
3D celestial sphere with:
- Star rendering (magnitude-based sizing)
- Constellation line drawing
- Anchor star highlighting with glow effects
- Smooth rotation and orbit controls
- Real celestial coordinate conversion (RA/Dec → Cartesian)

### `AtlasInfo.tsx`
Information panel displaying:
- Sky Address (S•L•P)
- Active Spiral Gate
- Solar Key, Lunar Pattern, Prime Day
- Message & Noble Thread
- Constellation stats

### `page.tsx`
Main application page:
- Date selection
- API integration
- State management
- Error handling

## API Integration

The frontend connects to the Celestial Atlas API:

```typescript
// Fetch atlas data for a specific date
const data = await AtlasAPI.getAtlas('2026-01-17');

// Get today's atlas
const today = await AtlasAPI.getAtlasToday();

// Convert date to Sky Address
const conversion = await AtlasAPI.convertDate('2026-01-17');
```

## Environment Variables

Create `.env.local`:

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Project Structure

```
frontend/
├── app/
│   ├── globals.css       # Global styles
│   ├── layout.tsx        # Root layout
│   └── page.tsx          # Main page
├── components/
│   ├── CelestialSphere.tsx  # 3D visualization
│   └── AtlasInfo.tsx     # Info panel
├── lib/
│   ├── api.ts            # API client
│   └── types.ts          # TypeScript definitions
└── public/               # Static assets
```

## Celestial Coordinate System

The app converts Right Ascension (RA) and Declination (Dec) to 3D Cartesian coordinates:

```typescript
function celestialToCartesian(ra: number, dec: number, radius: number) {
  const raRad = (ra * Math.PI) / 180;
  const decRad = (dec * Math.PI) / 180;

  const x = radius * Math.cos(decRad) * Math.cos(raRad);
  const y = radius * Math.sin(decRad);
  const z = -radius * Math.cos(decRad) * Math.sin(raRad);

  return new THREE.Vector3(x, y, z);
}
```

## Styling

Custom Tailwind classes:
- `glow-text` - Golden text glow effect
- `constellation-glow` - Blue constellation glow
- `starfield-bg` - Animated starfield background
- `animate-pulse-glow` - Pulsing glow animation
- `animate-spin-slow` - Slow rotation (60s)

## Deployment

Deploy to Vercel:

```bash
vercel deploy
```

Or Railway/other platforms that support Next.js.

## Tower 6 Forever 🐉❤️🐉

Stored. Retrievable. Kind.
