import React, { useState } from "react";
import { formatCurrency } from "../../lib/utils";

interface DataPoint {
  date: string;
  tvl: number;
  apy: number;
  sharpe: number;
}

const mockChartData: Record<string, DataPoint[]> = {
  "7D": [
    { date: "Nov 18", tvl: 1420000, apy: 9.8, sharpe: 1.15 },
    { date: "Nov 19", tvl: 1445000, apy: 10.1, sharpe: 1.20 },
    { date: "Nov 20", tvl: 1470000, apy: 10.2, sharpe: 1.22 },
    { date: "Nov 21", tvl: 1460000, apy: 10.0, sharpe: 1.18 },
    { date: "Nov 22", tvl: 1485000, apy: 10.3, sharpe: 1.25 },
    { date: "Nov 23", tvl: 1495000, apy: 10.4, sharpe: 1.26 },
    { date: "Nov 24", tvl: 1500000, apy: 10.45, sharpe: 1.28 },
  ],
  "30D": [
    { date: "Oct 25", tvl: 1100000, apy: 8.5, sharpe: 0.95 },
    { date: "Nov 01", tvl: 1220000, apy: 9.1, sharpe: 1.05 },
    { date: "Nov 08", tvl: 1340000, apy: 9.6, sharpe: 1.12 },
    { date: "Nov 15", tvl: 1410000, apy: 9.9, sharpe: 1.18 },
    { date: "Nov 24", tvl: 1500000, apy: 10.45, sharpe: 1.28 },
  ],
};

export function InteractiveChart() {
  const [timeframe, setTimeframe] = useState<"7D" | "30D">("7D");
  const [activeMetric, setActiveMetric] = useState<"tvl" | "apy">("tvl");
  const [hoveredPoint, setHoveredPoint] = useState<DataPoint | null>(null);

  const data = mockChartData[timeframe];
  const minVal = Math.min(...data.map((d) => (activeMetric === "tvl" ? d.tvl : d.apy)));
  const maxVal = Math.max(...data.map((d) => (activeMetric === "tvl" ? d.tvl : d.apy)));

  const width = 600;
  const height = 120;
  const padding = 12;

  const points = data.map((d, i) => {
    const val = activeMetric === "tvl" ? d.tvl : d.apy;
    const x = padding + (i / (data.length - 1)) * (width - padding * 2);
    const y = height - padding - ((val - minVal) / (maxVal - minVal || 1)) * (height - padding * 2);
    return { x, y, data: d };
  });

  const pathD = points.reduce((acc, curr, idx, arr) => {
    if (idx === 0) return `M ${curr.x} ${curr.y}`;
    const prev = arr[idx - 1];
    const cpX1 = prev.x + (curr.x - prev.x) / 2;
    const cpY1 = prev.y;
    const cpX2 = prev.x + (curr.x - prev.x) / 2;
    const cpY2 = curr.y;
    return `${acc} C ${cpX1} ${cpY1}, ${cpX2} ${cpY2}, ${curr.x} ${curr.y}`;
  }, "");

  const areaD = `${pathD} L ${points[points.length - 1].x} ${height} L ${points[0].x} ${height} Z`;

  return (
    <div className="zinc-card rounded-xl p-3.5 border border-zinc-800">
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center gap-3">
          <span className="text-xs font-bold text-white font-mono uppercase tracking-wider">
            Historical Trajectory
          </span>
          <span className="text-sm font-bold font-mono text-emerald-400">
            {hoveredPoint
              ? activeMetric === "tvl"
                ? formatCurrency(hoveredPoint.tvl)
                : `${hoveredPoint.apy.toFixed(2)}% APY`
              : activeMetric === "tvl"
              ? formatCurrency(data[data.length - 1].tvl)
              : `${data[data.length - 1].apy.toFixed(2)}% APY`}
          </span>
          <span className="text-[10px] text-zinc-500 font-mono">
            {hoveredPoint ? `(${hoveredPoint.date})` : "(Current)"}
          </span>
        </div>

        <div className="flex items-center gap-2">
          <div className="flex bg-zinc-900 p-0.5 rounded border border-zinc-800 text-[11px] font-mono">
            <button
              onClick={() => setActiveMetric("tvl")}
              className={`px-2 py-0.5 rounded ${activeMetric === "tvl" ? "bg-zinc-800 text-white font-bold" : "text-zinc-400"}`}
            >
              TVL
            </button>
            <button
              onClick={() => setActiveMetric("apy")}
              className={`px-2 py-0.5 rounded ${activeMetric === "apy" ? "bg-zinc-800 text-white font-bold" : "text-zinc-400"}`}
            >
              APY
            </button>
          </div>

          <div className="flex bg-zinc-900 p-0.5 rounded border border-zinc-800 text-[11px] font-mono">
            {(["7D", "30D"] as const).map((tf) => (
              <button
                key={tf}
                onClick={() => setTimeframe(tf)}
                className={`px-2 py-0.5 rounded ${timeframe === tf ? "bg-zinc-800 text-white font-bold" : "text-zinc-400"}`}
              >
                {tf}
              </button>
            ))}
          </div>
        </div>
      </div>

      <div className="w-full h-28 relative">
        <svg viewBox={`0 0 ${width} ${height}`} className="w-full h-full" preserveAspectRatio="none">
          <defs>
            <linearGradient id="chartGradientZinc" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#3b82f6" stopOpacity="0.2" />
              <stop offset="100%" stopColor="#3b82f6" stopOpacity="0.0" />
            </linearGradient>
          </defs>
          <path d={areaD} fill="url(#chartGradientZinc)" />
          <path d={pathD} fill="none" stroke="#3b82f6" strokeWidth="2" strokeLinecap="round" />
          {points.map((pt, idx) => (
            <circle
              key={idx}
              cx={pt.x}
              cy={pt.y}
              r="3"
              className="fill-blue-500 stroke-zinc-950 stroke-2 hover:r-5 hover:fill-white transition-all cursor-pointer"
              onMouseEnter={() => setHoveredPoint(pt.data)}
              onMouseLeave={() => setHoveredPoint(null)}
            />
          ))}
        </svg>
      </div>
    </div>
  );
}
