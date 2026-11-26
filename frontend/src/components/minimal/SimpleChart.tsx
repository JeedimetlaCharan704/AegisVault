import React, { useState } from "react";
import { formatCurrency } from "../../lib/utils";
import { SpotlightCard } from "../magic/SpotlightCard";

interface DataPoint {
  date: string;
  tvl: number;
}

const dataMap: Record<string, DataPoint[]> = {
  "7D": [
    { date: "Nov 18", tvl: 1420000 },
    { date: "Nov 19", tvl: 1445000 },
    { date: "Nov 20", tvl: 1470000 },
    { date: "Nov 21", tvl: 1460000 },
    { date: "Nov 22", tvl: 1485000 },
    { date: "Nov 23", tvl: 1495000 },
    { date: "Nov 24", tvl: 1500000 },
  ],
  "30D": [
    { date: "Oct 25", tvl: 1100000 },
    { date: "Nov 01", tvl: 1220000 },
    { date: "Nov 08", tvl: 1340000 },
    { date: "Nov 15", tvl: 1410000 },
    { date: "Nov 24", tvl: 1500000 },
  ],
};

export function SimpleChart() {
  const [timeframe, setTimeframe] = useState<"7D" | "30D">("7D");
  const [hovered, setHovered] = useState<DataPoint | null>(null);

  const data = dataMap[timeframe];
  const minVal = Math.min(...data.map((d) => d.tvl));
  const maxVal = Math.max(...data.map((d) => d.tvl));

  const width = 850;
  const height = 210;
  const padding = 20;

  const points = data.map((d, i) => {
    const x = padding + (i / (data.length - 1)) * (width - padding * 2);
    const y = height - padding - ((d.tvl - minVal) / (maxVal - minVal || 1)) * (height - padding * 2);
    return { x, y, data: d };
  });

  const pathD = points.reduce((acc, curr, idx, arr) => {
    if (idx === 0) return `M ${curr.x} ${curr.y}`;
    const prev = arr[idx - 1];
    const cpX = prev.x + (curr.x - prev.x) / 2;
    return `${acc} C ${cpX} ${prev.y}, ${cpX} ${curr.y}, ${curr.x} ${curr.y}`;
  }, "");

  const areaD = `${pathD} L ${points[points.length - 1].x} ${height} L ${points[0].x} ${height} Z`;

  return (
    <SpotlightCard className="p-6 sm:p-7 w-full flex flex-col justify-between" spotlightColor="rgba(59, 130, 246, 0.12)">
      <div className="flex items-center justify-between mb-5">
        <div>
          <span className="text-[11px] font-mono text-zinc-400 uppercase tracking-wider block">
            Vault Performance Trajectory
          </span>
          <span className="text-2xl font-semibold font-mono text-white mt-1 block tracking-tight">
            {hovered ? formatCurrency(hovered.tvl) : formatCurrency(data[data.length - 1].tvl)}
            {hovered && (
              <span className="text-xs text-zinc-400 font-normal ml-2 font-mono">({hovered.date})</span>
            )}
          </span>
        </div>

        <div className="flex bg-zinc-900 p-1 rounded-lg border border-white/[0.08] text-xs font-mono">
          {(["7D", "30D"] as const).map((tf) => (
            <button
              key={tf}
              onClick={() => setTimeframe(tf)}
              className={`px-3.5 py-1.5 rounded-md transition-all ${
                timeframe === tf ? "bg-zinc-800 text-white font-semibold shadow-sm" : "text-zinc-400 hover:text-zinc-200"
              }`}
            >
              {tf}
            </button>
          ))}
        </div>
      </div>

      {/* Spacious SVG Graphic */}
      <div className="w-full h-48 sm:h-52 relative my-2">
        <svg viewBox={`0 0 ${width} ${height}`} className="w-full h-full overflow-visible" preserveAspectRatio="none">
          <defs>
            <linearGradient id="minimalGrad" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#3b82f6" stopOpacity="0.18" />
              <stop offset="100%" stopColor="#3b82f6" stopOpacity="0.0" />
            </linearGradient>
          </defs>
          <path d={areaD} fill="url(#minimalGrad)" />
          <path d={pathD} fill="none" stroke="#60a5fa" strokeWidth="2.5" strokeLinecap="round" />
          {points.map((pt, i) => (
            <circle
              key={i}
              cx={pt.x}
              cy={pt.y}
              r="4"
              className="fill-blue-400 stroke-[#08090c] stroke-2 hover:r-6 hover:fill-white cursor-pointer transition-all"
              onMouseEnter={() => setHovered(pt.data)}
              onMouseLeave={() => setHovered(null)}
            />
          ))}
        </svg>
      </div>

      <div className="flex items-center justify-between text-xs font-mono text-zinc-400 pt-4 border-t border-white/[0.06]">
        <span>Validated by InvariantGuard on Base Sepolia</span>
        <span>Rebalancing Cadence: Real-time Adaptive</span>
      </div>
    </SpotlightCard>
  );
}
