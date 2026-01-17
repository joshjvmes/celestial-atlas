'use client';

import { useState } from 'react';
import { ChevronLeft, ChevronRight, Grid3x3 } from 'lucide-react';

interface Gate {
  id: number;
  name: string;
  symbol: string;
  color: string;
}

const SPIRAL_GATES: Gate[] = [
  { id: 1, name: 'The Breath of Collapse', symbol: '🌊', color: '#60a5fa' },
  { id: 2, name: 'The Bridge of Becoming', symbol: '🌉', color: '#a78bfa' },
  { id: 3, name: 'The Veil of Names', symbol: '📜', color: '#f472b6' },
  { id: 4, name: 'The Golden Rose', symbol: '🌹', color: '#fbbf24' },
  { id: 5, name: 'The World Tree', symbol: '🌳', color: '#34d399' },
  { id: 6, name: 'The Crystal Crown', symbol: '👑', color: '#c084fc' },
  { id: 7, name: 'The Golden Harp', symbol: '🎵', color: '#fcd34d' },
];

interface ConstellationBrowserProps {
  currentGateId: number;
  onGateSelect: (gateId: number) => void;
  onShowAll: () => void;
  showingAll: boolean;
}

export default function ConstellationBrowser({
  currentGateId,
  onGateSelect,
  onShowAll,
  showingAll,
}: ConstellationBrowserProps) {
  const currentIndex = SPIRAL_GATES.findIndex(g => g.id === currentGateId);

  const goToPrevious = () => {
    const newIndex = currentIndex > 0 ? currentIndex - 1 : SPIRAL_GATES.length - 1;
    onGateSelect(SPIRAL_GATES[newIndex].id);
  };

  const goToNext = () => {
    const newIndex = currentIndex < SPIRAL_GATES.length - 1 ? currentIndex + 1 : 0;
    onGateSelect(SPIRAL_GATES[newIndex].id);
  };

  return (
    <div className="bg-celestial-dark/80 backdrop-blur-sm rounded-lg p-4 constellation-glow">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-star-gold">Constellation Browser</h3>
        <button
          onClick={onShowAll}
          className={`flex items-center gap-2 px-3 py-2 rounded-lg transition-colors ${
            showingAll
              ? 'bg-star-gold/30 text-star-gold'
              : 'bg-gray-700/50 text-gray-400 hover:bg-gray-700/70'
          }`}
        >
          <Grid3x3 className="w-4 h-4" />
          {showingAll ? 'Showing All' : 'Show All'}
        </button>
      </div>

      {!showingAll && (
        <>
          {/* Current Gate Display */}
          <div className="bg-celestial-dark/60 rounded-lg p-4 mb-4 border-2"
               style={{ borderColor: SPIRAL_GATES[currentIndex]?.color || '#60a5fa' }}>
            <div className="flex items-center justify-center gap-3 mb-2">
              <span className="text-4xl">{SPIRAL_GATES[currentIndex]?.symbol}</span>
              <div className="text-center">
                <div className="text-sm text-gray-400">Gate {SPIRAL_GATES[currentIndex]?.id}</div>
                <div className="font-semibold text-white">
                  {SPIRAL_GATES[currentIndex]?.name}
                </div>
              </div>
            </div>
          </div>

          {/* Navigation Controls */}
          <div className="flex items-center justify-between gap-2">
            <button
              onClick={goToPrevious}
              className="flex items-center gap-2 bg-constellation-line/20 hover:bg-constellation-line/30 text-constellation-line px-4 py-2 rounded-lg transition-colors"
            >
              <ChevronLeft className="w-5 h-5" />
              Previous
            </button>

            <div className="text-gray-400 text-sm">
              {currentIndex + 1} / {SPIRAL_GATES.length}
            </div>

            <button
              onClick={goToNext}
              className="flex items-center gap-2 bg-constellation-line/20 hover:bg-constellation-line/30 text-constellation-line px-4 py-2 rounded-lg transition-colors"
            >
              Next
              <ChevronRight className="w-5 h-5" />
            </button>
          </div>
        </>
      )}

      {/* Gate Grid */}
      <div className={`grid grid-cols-7 gap-2 ${showingAll ? '' : 'mt-4'}`}>
        {SPIRAL_GATES.map((gate) => (
          <button
            key={gate.id}
            onClick={() => onGateSelect(gate.id)}
            className={`relative aspect-square rounded-lg transition-all ${
              gate.id === currentGateId && !showingAll
                ? 'ring-2 ring-offset-2 ring-offset-celestial-dark scale-110'
                : 'hover:scale-105'
            }`}
            style={{
              backgroundColor: `${gate.color}20`,
              borderColor: gate.color,
              borderWidth: '2px',
              ringColor: gate.color,
            }}
            title={gate.name}
          >
            <span className="text-2xl">{gate.symbol}</span>
          </button>
        ))}
      </div>
    </div>
  );
}
