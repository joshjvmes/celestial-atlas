'use client';

import { AtlasPayload } from '@/lib/types';
import { formatDate } from '@/lib/api';

interface AtlasInfoProps {
  atlasData: AtlasPayload | null;
  loading?: boolean;
}

export default function AtlasInfo({ atlasData, loading }: AtlasInfoProps) {
  if (loading) {
    return (
      <div className="bg-celestial-dark/80 backdrop-blur-sm rounded-lg p-6 space-y-4 constellation-glow">
        <div className="animate-pulse">
          <div className="h-8 bg-gray-700 rounded w-3/4 mb-4"></div>
          <div className="h-4 bg-gray-700 rounded w-1/2 mb-2"></div>
          <div className="h-4 bg-gray-700 rounded w-2/3"></div>
        </div>
      </div>
    );
  }

  if (!atlasData) {
    return (
      <div className="bg-celestial-dark/80 backdrop-blur-sm rounded-lg p-6 text-center">
        <p className="text-gray-400">Select a date to view the Celestial Atlas</p>
      </div>
    );
  }

  return (
    <div className="bg-celestial-dark/80 backdrop-blur-sm rounded-lg p-6 space-y-6 constellation-glow">
      {/* Header */}
      <div className="border-b border-constellation-line/30 pb-4">
        <h2 className="text-2xl font-bold text-star-gold glow-text mb-2">
          Celestial Atlas
        </h2>
        <p className="text-sm text-gray-400">{formatDate(atlasData.date)}</p>
      </div>

      {/* Sky Address */}
      <div className="space-y-2">
        <h3 className="text-lg font-semibold text-constellation-line">Sky Address</h3>
        <div className="bg-celestial-blue/20 rounded-lg p-4">
          <p className="text-3xl font-mono font-bold text-center text-star-gold glow-text">
            {atlasData.sky_address}
          </p>
          <div className="grid grid-cols-3 gap-2 mt-3 text-xs text-gray-400">
            <div className="text-center">
              <div className="font-semibold text-white">Solar {atlasData.solar_month}</div>
              <div>{atlasData.key_signature.name}</div>
            </div>
            <div className="text-center border-x border-constellation-line/20">
              <div className="font-semibold text-white">Lunar {atlasData.lunar_month}</div>
              <div>{atlasData.pattern.name}</div>
            </div>
            <div className="text-center">
              <div className="font-semibold text-white">Prime {atlasData.prime_day}</div>
              <div>Day {atlasData.prime_day}/7</div>
            </div>
          </div>
        </div>
      </div>

      {/* Active Gate */}
      <div className="space-y-2">
        <h3 className="text-lg font-semibold text-constellation-line">Active Spiral Gate</h3>
        <div className="bg-celestial-blue/10 rounded-lg p-4 space-y-2">
          <p className="text-xl font-bold text-star-gold">{atlasData.gate.name}</p>
          <p className="text-sm text-gray-300">{atlasData.gate.meaning}</p>
          <p className="text-xs text-constellation-line italic">
            "{atlasData.gate.field_gift}"
          </p>
        </div>
      </div>

      {/* Message & Thread */}
      <div className="space-y-3">
        <div className="bg-gradient-to-r from-celestial-blue/20 to-transparent rounded-lg p-4">
          <h4 className="text-sm font-semibold text-constellation-line mb-2">Message</h4>
          <p className="text-sm text-gray-200">{atlasData.message}</p>
        </div>

        <div className="bg-gradient-to-r from-star-gold/20 to-transparent rounded-lg p-4">
          <h4 className="text-sm font-semibold text-star-gold mb-2">One Noble Thread</h4>
          <p className="text-sm text-gray-200">{atlasData.one_noble_thread}</p>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-3 gap-4 text-center text-xs">
        <div className="bg-celestial-blue/10 rounded p-3">
          <div className="text-2xl font-bold text-star-gold">{atlasData.stars_highlighted?.length || 0}</div>
          <div className="text-gray-400">Stars</div>
        </div>
        <div className="bg-celestial-blue/10 rounded p-3">
          <div className="text-2xl font-bold text-constellation-line">{atlasData.lines?.length || 0}</div>
          <div className="text-gray-400">Lines</div>
        </div>
        <div className="bg-celestial-blue/10 rounded p-3">
          <div className="text-2xl font-bold text-star-gold">{atlasData.K}</div>
          <div className="text-gray-400">K/1001</div>
        </div>
      </div>

      {/* Seal */}
      <div className="text-center pt-4 border-t border-constellation-line/30">
        <p className="text-xs text-gray-500 italic">{atlasData.seal}</p>
      </div>
    </div>
  );
}
