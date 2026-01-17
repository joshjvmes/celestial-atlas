// Celestial Atlas API Client

import { AtlasPayload, SkyAddressConversion } from './types';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export class AtlasAPI {
  static async getAtlas(date: string): Promise<AtlasPayload> {
    const response = await fetch(`${API_URL}/atlas?date=${date}`);
    if (!response.ok) {
      throw new Error(`Failed to fetch atlas: ${response.statusText}`);
    }
    return response.json();
  }

  static async getAtlasToday(): Promise<AtlasPayload> {
    const response = await fetch(`${API_URL}/atlas/today`);
    if (!response.ok) {
      throw new Error(`Failed to fetch today's atlas: ${response.statusText}`);
    }
    return response.json();
  }

  static async convertDate(date: string): Promise<SkyAddressConversion> {
    const response = await fetch(`${API_URL}/atlas/convert?date=${date}`);
    if (!response.ok) {
      throw new Error(`Failed to convert date: ${response.statusText}`);
    }
    return response.json();
  }

  static async getGates() {
    const response = await fetch(`${API_URL}/atlas/gates`);
    if (!response.ok) {
      throw new Error(`Failed to fetch gates: ${response.statusText}`);
    }
    return response.json();
  }

  static async getAtlasByCoordinate(S: number, L: number, P: number): Promise<AtlasPayload> {
    const response = await fetch(`${API_URL}/atlas/coordinate?S=${S}&L=${L}&P=${P}`);
    if (!response.ok) {
      throw new Error(`Failed to fetch atlas by coordinate: ${response.statusText}`);
    }
    return response.json();
  }
}

// Helper functions
export function formatSkyAddress(S: number, L: number, P: number): string {
  return `${S}•${L}•${P}`;
}

export function formatDate(dateStr: string): string {
  const date = new Date(dateStr);
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
}
