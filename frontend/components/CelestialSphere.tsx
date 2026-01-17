'use client';

import { useRef, useMemo, Suspense } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Stars } from '@react-three/drei';
import * as THREE from 'three';
import { Star as StarType, AtlasPayload } from '@/lib/types';

interface CelestialSphereProps {
  atlasData: AtlasPayload | null;
  allGatesData?: AtlasPayload[];
  rotating?: boolean;
  showOverlay?: boolean;
}

// Mapping of Prime Day (P) / Gate to constellation overlay images
const CONSTELLATION_OVERLAYS: { [key: number]: string } = {
  1: '/constellations/crystal-crown-wave.png',  // The Breath of Collapse
  2: '/constellations/soaring-songbird.png',    // The Bridge of Becoming
  3: '/constellations/ship-of-the-veiled-void.png', // The Veil of Names
  4: '/constellations/golden-rose.png',         // The Golden Rose
  5: '/constellations/world-tree.png',          // The World Tree
  6: '/constellations/trumpet.png',             // The Crystal Crown
  7: '/constellations/golden-harp.png',         // The Golden Harp
};

// Convert celestial coordinates (RA/Dec) to Cartesian (x, y, z)
function celestialToCartesian(ra: number, dec: number, radius: number = 10) {
  const raRad = (ra * Math.PI) / 180;
  const decRad = (dec * Math.PI) / 180;

  const x = radius * Math.cos(decRad) * Math.cos(raRad);
  const y = radius * Math.sin(decRad);
  const z = -radius * Math.cos(decRad) * Math.sin(raRad);

  return new THREE.Vector3(x, y, z);
}

// Individual Star Component
function StarPoint({ star, isHighlighted }: { star: StarType; isHighlighted: boolean }) {
  const position = useMemo(
    () => celestialToCartesian(star.ra, star.dec, 10),
    [star.ra, star.dec]
  );

  const size = useMemo(() => {
    // Size based on magnitude (brighter = larger)
    const baseSize = star.is_anchor ? 0.15 : 0.08;
    const magnitudeFactor = Math.max(0.3, 1 - star.magnitude / 6);
    return baseSize * magnitudeFactor;
  }, [star.magnitude, star.is_anchor]);

  const color = star.is_anchor ? '#fbbf24' : isHighlighted ? '#60a5fa' : '#ffffff';

  return (
    <mesh position={position}>
      <sphereGeometry args={[size, 16, 16]} />
      <meshBasicMaterial
        color={color}
        transparent
        opacity={isHighlighted ? 0.9 : 0.6}
      />
      {isHighlighted && (
        <pointLight
          color={star.is_anchor ? '#fbbf24' : '#60a5fa'}
          intensity={star.is_anchor ? 2 : 1}
          distance={3}
        />
      )}
    </mesh>
  );
}

// Constellation Line Component
function ConstellationLine({
  start,
  end,
  stars
}: {
  start: string;
  end: string;
  stars: StarType[]
}) {
  const startStar = stars.find(s => s.id === start);
  const endStar = stars.find(s => s.id === end);

  const points = useMemo(() => {
    if (!startStar || !endStar) return [];

    const p1 = celestialToCartesian(startStar.ra, startStar.dec, 10);
    const p2 = celestialToCartesian(endStar.ra, endStar.dec, 10);

    return [p1, p2];
  }, [startStar, endStar]);

  if (points.length === 0) return null;

  return (
    <line>
      <bufferGeometry>
        <bufferAttribute
          attach="attributes-position"
          count={points.length}
          array={new Float32Array(points.flatMap(p => [p.x, p.y, p.z]))}
          itemSize={3}
        />
      </bufferGeometry>
      <lineBasicMaterial color="#60a5fa" transparent opacity={0.7} linewidth={2} />
    </line>
  );
}

// Rotating Sphere Grid
function SphereGrid({ rotating }: { rotating: boolean }) {
  const meshRef = useRef<THREE.Mesh>(null);

  useFrame((state, delta) => {
    if (meshRef.current && rotating) {
      meshRef.current.rotation.y += delta * 0.1;
    }
  });

  return (
    <mesh ref={meshRef}>
      <sphereGeometry args={[9.5, 32, 32]} />
      <meshBasicMaterial
        color="#1e3a8a"
        wireframe
        transparent
        opacity={0.1}
      />
    </mesh>
  );
}

// Gate colors for "Show All" mode
const GATE_COLORS = ['#60a5fa', '#a78bfa', '#f472b6', '#fbbf24', '#34d399', '#c084fc', '#fcd34d'];

// Main Scene
function Scene({
  atlasData,
  allGatesData,
  rotating
}: {
  atlasData: AtlasPayload | null;
  allGatesData?: AtlasPayload[];
  rotating: boolean
}) {
  const highlightedStarIds = useMemo(() => {
    if (!atlasData || !atlasData.stars_highlighted) return new Set<string>();
    return new Set(atlasData.stars_highlighted.map(s => s.id));
  }, [atlasData]);

  return (
    <>
      <color attach="background" args={['#0a0e27']} />
      <ambientLight intensity={0.3} />

      {/* Background stars */}
      <Stars
        radius={100}
        depth={50}
        count={5000}
        factor={4}
        saturation={0}
        fade
        speed={rotating ? 0.5 : 0}
      />

      {/* Celestial sphere grid */}
      <SphereGrid rotating={rotating} />

      {/* Show All Gates Mode */}
      {allGatesData && allGatesData.length > 0 ? (
        allGatesData.map((gateData, gateIndex) => (
          <group key={`gate-${gateIndex}`}>
            {/* Stars for this gate */}
            {gateData.stars_highlighted.map((star) => {
              const position = celestialToCartesian(star.ra, star.dec, 10);
              const baseSize = star.is_anchor ? 0.12 : 0.06;
              const magnitudeFactor = Math.max(0.3, 1 - star.magnitude / 6);
              const size = baseSize * magnitudeFactor;
              const color = GATE_COLORS[gateIndex] || '#ffffff';

              return (
                <mesh key={`${gateIndex}-${star.id}`} position={position}>
                  <sphereGeometry args={[size, 16, 16]} />
                  <meshBasicMaterial
                    color={color}
                    transparent
                    opacity={0.7}
                  />
                </mesh>
              );
            })}

            {/* Constellation lines for this gate */}
            {gateData.lines.map(([start, end], lineIdx) => {
              const startStar = gateData.stars_highlighted.find(s => s.id === start);
              const endStar = gateData.stars_highlighted.find(s => s.id === end);

              if (!startStar || !endStar) return null;

              const p1 = celestialToCartesian(startStar.ra, startStar.dec, 10);
              const p2 = celestialToCartesian(endStar.ra, endStar.dec, 10);

              return (
                <line key={`${gateIndex}-line-${lineIdx}`}>
                  <bufferGeometry>
                    <bufferAttribute
                      attach="attributes-position"
                      count={2}
                      array={new Float32Array([p1.x, p1.y, p1.z, p2.x, p2.y, p2.z])}
                      itemSize={3}
                    />
                  </bufferGeometry>
                  <lineBasicMaterial
                    color={GATE_COLORS[gateIndex] || '#60a5fa'}
                    transparent
                    opacity={0.5}
                    linewidth={2}
                  />
                </line>
              );
            })}
          </group>
        ))
      ) : (
        <>
          {/* Single constellation mode */}
          {atlasData?.stars_highlighted?.map((star) => (
            <StarPoint
              key={star.id}
              star={star}
              isHighlighted={true}
            />
          ))}

          {atlasData?.lines?.map(([start, end], idx) => (
            <ConstellationLine
              key={`line-${idx}`}
              start={start}
              end={end}
              stars={atlasData.stars_highlighted || []}
            />
          ))}
        </>
      )}

      {/* Camera controls */}
      <OrbitControls
        enableZoom={true}
        enablePan={false}
        minDistance={12}
        maxDistance={30}
        autoRotate={rotating}
        autoRotateSpeed={0.5}
      />
    </>
  );
}

// Main Component Export
export default function CelestialSphere({ atlasData, allGatesData, rotating = false, showOverlay = false }: CelestialSphereProps) {
  const overlayImage = atlasData && !allGatesData ? CONSTELLATION_OVERLAYS[atlasData.P] : null;

  console.log('CelestialSphere:', { showOverlay, overlayImage, P: atlasData?.P, hasAllGates: !!allGatesData });

  return (
    <div className="w-full h-full relative">
      <Canvas
        camera={{ position: [0, 0, 20], fov: 60 }}
        gl={{ antialias: true, alpha: true }}
      >
        <Suspense fallback={null}>
          <Scene atlasData={atlasData} allGatesData={allGatesData} rotating={rotating} />
        </Suspense>
      </Canvas>

      {/* Constellation Overlay */}
      {showOverlay && overlayImage && (
        <div className="absolute inset-0 pointer-events-none flex items-center justify-center z-10">
          <img
            src={overlayImage}
            alt="Constellation overlay"
            className="max-w-[80%] max-h-[80%] object-contain opacity-60 mix-blend-screen"
            style={{
              filter: 'drop-shadow(0 0 20px rgba(96, 165, 250, 0.5))',
            }}
          />
        </div>
      )}
    </div>
  );
}
