// Celestial Atlas Type Definitions

export interface Star {
  id: string;
  name: string;
  ra: number;
  dec: number;
  magnitude: number;
  is_anchor: boolean;
}

export interface Gate {
  id: number;
  name: string;
  meaning: string;
  function: string;
  field_gift: string;
}

export interface Pattern {
  lunar_id: number;
  name: string;
  description: string;
  prime_step: number;
}

export interface KeySignature {
  solar_id: number;
  name: string;
  render_bias: string;
  mood: string;
}

export interface RenderSettings {
  intensity: number;
  max_stars: number;
  max_lines: number;
  glow_mode: string;
  line_mode: string;
}

export interface AtlasPayload {
  date: string;
  anchor_date: string;
  K: number;
  sky_address: string;
  solar_month: number;
  lunar_month: number;
  prime_day: number;
  S: number;  // Shorthand for solar_month
  L: number;  // Shorthand for lunar_month
  P: number;  // Shorthand for prime_day
  gate: Gate;
  pattern: Pattern;
  key_signature: KeySignature;
  stars_highlighted: Star[];
  lines: [string, string][];
  render: RenderSettings;
  message: string;
  one_noble_thread: string;
  seal: string;
}

export interface SkyAddressConversion {
  date: string;
  sky_address: string;
  solar_month: number;
  lunar_month: number;
  prime_day: number;
  K: number;
  spiral_position: string;
  seal: string;
}
