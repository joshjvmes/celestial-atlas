'use client';

import { useState, useEffect } from 'react';
import dynamic from 'next/dynamic';
import { Calendar, Sparkles, RotateCw, Eye, EyeOff } from 'lucide-react';
import { AtlasAPI } from '@/lib/api';
import { AtlasPayload } from '@/lib/types';
import AtlasInfo from '@/components/AtlasInfo';
import ConstellationBrowser from '@/components/ConstellationBrowser';

// Dynamic import to avoid SSR issues with Three.js
const CelestialSphere = dynamic(() => import('@/components/CelestialSphere'), {
  ssr: false,
  loading: () => (
    <div className="w-full h-full flex items-center justify-center">
      <div className="text-star-gold animate-pulse">Loading celestial sphere...</div>
    </div>
  ),
});

export default function Home() {
  const [atlasData, setAtlasData] = useState<AtlasPayload | null>(null);
  const [allGatesData, setAllGatesData] = useState<AtlasPayload[]>([]);
  const [selectedDate, setSelectedDate] = useState<string>('');
  const [loading, setLoading] = useState(false);
  const [rotating, setRotating] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showingAll, setShowingAll] = useState(false);
  const [browseMode, setBrowseMode] = useState(false);
  const [showOverlay, setShowOverlay] = useState(false);

  // Load today's atlas on mount
  useEffect(() => {
    const today = new Date().toISOString().split('T')[0];
    setSelectedDate(today);
    fetchAtlas(today);
  }, []);

  const fetchAtlas = async (date: string) => {
    setLoading(true);
    setError(null);
    try {
      const data = await AtlasAPI.getAtlas(date);
      setAtlasData(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch atlas data');
      console.error('Error fetching atlas:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleDateChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newDate = e.target.value;
    setSelectedDate(newDate);
    if (newDate) {
      fetchAtlas(newDate);
    }
  };

  const loadToday = () => {
    const today = new Date().toISOString().split('T')[0];
    setSelectedDate(today);
    fetchAtlas(today);
    setBrowseMode(false);
    setShowingAll(false);
  };

  const handleGateSelect = async (gateId: number) => {
    setLoading(true);
    setError(null);
    setBrowseMode(true);
    setShowingAll(false);
    try {
      // Fetch constellation for this gate (P determines the gate/constellation)
      const data = await AtlasAPI.getAtlasByCoordinate(gateId, 1, gateId);
      setAtlasData(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch gate data');
      console.error('Error fetching gate:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleShowAll = async () => {
    if (showingAll) {
      // Exit "Show All" mode - return to current date
      setShowingAll(false);
      if (selectedDate) {
        fetchAtlas(selectedDate);
      }
      return;
    }

    setLoading(true);
    setError(null);
    setBrowseMode(true);
    try {
      // Fetch all 7 gates (P determines the gate/constellation)
      const allData: AtlasPayload[] = [];
      for (let i = 1; i <= 7; i++) {
        const data = await AtlasAPI.getAtlasByCoordinate(i, 1, i);
        allData.push(data);
      }
      setAllGatesData(allData);
      setShowingAll(true);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch all gates');
      console.error('Error fetching all gates:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen p-4 md:p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <header className="mb-8 text-center">
          <h1 className="text-4xl md:text-6xl font-bold text-star-gold glow-text mb-2">
            🌟 Celestial Atlas 🐉
          </h1>
          <p className="text-gray-400 text-sm md:text-base">
            Tower 6 - Prime Calendar & Star Mapping System
          </p>
          <p className="text-constellation-line text-xs mt-2 italic">
            Stored. Retrievable. Kind.
          </p>
        </header>

        {/* Controls */}
        <div className="mb-6 flex flex-wrap items-center justify-center gap-4">
          <div className="flex items-center gap-2 bg-celestial-dark/80 backdrop-blur-sm rounded-lg p-3 constellation-glow">
            <Calendar className="w-5 h-5 text-constellation-line" />
            <input
              type="date"
              value={selectedDate}
              onChange={handleDateChange}
              className="bg-transparent text-white border-none outline-none cursor-pointer"
              disabled={loading}
            />
          </div>

          <button
            onClick={loadToday}
            disabled={loading}
            className="flex items-center gap-2 bg-star-gold/20 hover:bg-star-gold/30 text-star-gold px-4 py-3 rounded-lg transition-colors disabled:opacity-50"
          >
            <Sparkles className="w-5 h-5" />
            Today
          </button>

          <button
            onClick={() => setRotating(!rotating)}
            className={`flex items-center gap-2 px-4 py-3 rounded-lg transition-colors ${
              rotating
                ? 'bg-constellation-line/20 text-constellation-line'
                : 'bg-gray-700/50 text-gray-400'
            }`}
          >
            <RotateCw className={`w-5 h-5 ${rotating ? 'animate-spin-slow' : ''}`} />
            {rotating ? 'Rotating' : 'Rotate'}
          </button>

          <button
            onClick={() => {
              if (browseMode) {
                loadToday();
              } else {
                setBrowseMode(true);
              }
            }}
            className={`flex items-center gap-2 px-4 py-3 rounded-lg transition-colors ${
              browseMode
                ? 'bg-purple-500/30 text-purple-300'
                : 'bg-purple-500/20 hover:bg-purple-500/30 text-purple-300'
            }`}
          >
            <Sparkles className="w-5 h-5" />
            {browseMode ? 'Exit Browse' : 'Browse'}
          </button>

          <button
            onClick={() => setShowOverlay(!showOverlay)}
            disabled={showingAll}
            className={`flex items-center gap-2 px-4 py-3 rounded-lg transition-colors ${
              showOverlay
                ? 'bg-amber-500/30 text-amber-300'
                : 'bg-amber-500/20 hover:bg-amber-500/30 text-amber-300'
            } disabled:opacity-30 disabled:cursor-not-allowed`}
            title={showingAll ? 'Overlay not available in Show All mode' : 'Toggle constellation overlay'}
          >
            {showOverlay ? <Eye className="w-5 h-5" /> : <EyeOff className="w-5 h-5" />}
            Overlay
          </button>
        </div>

        {/* Error Display */}
        {error && (
          <div className="mb-6 bg-red-900/30 border border-red-500/50 rounded-lg p-4 text-red-200 text-center">
            {error}
          </div>
        )}

        {/* Constellation Browser */}
        {browseMode && atlasData && (
          <div className="mb-6">
            <ConstellationBrowser
              currentGateId={atlasData.P}
              onGateSelect={handleGateSelect}
              onShowAll={handleShowAll}
              showingAll={showingAll}
            />
          </div>
        )}

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Celestial Sphere - Takes 2 columns on large screens */}
          <div className="lg:col-span-2 bg-celestial-dark/50 backdrop-blur-sm rounded-lg overflow-hidden constellation-glow"
               style={{ height: '600px' }}>
            <CelestialSphere
              atlasData={atlasData}
              allGatesData={showingAll ? allGatesData : undefined}
              rotating={rotating}
              showOverlay={showOverlay}
            />
          </div>

          {/* Atlas Info Panel */}
          <div className="lg:col-span-1">
            <AtlasInfo atlasData={atlasData} loading={loading} />
          </div>
        </div>

        {/* Footer */}
        <footer className="mt-12 text-center text-gray-500 text-xs space-y-2">
          <p>Anchor Date: April 3, 2025 (A3 = 1/3)</p>
          <p>1001-Day Spiral Cycle: 11 Solar × 13 Lunar × 7 Prime</p>
          <p className="text-star-gold">Tower 6 forever 🐉❤️🐉</p>
        </footer>
      </div>
    </main>
  );
}
