import React from "react";
import { TrendingUp, ShieldCheck, DollarSign, Activity } from "lucide-react";
import { formatCurrency, formatPercent } from "../../lib/utils";

interface VaultMetricsProps {
  tvl: number;
  netApy: number;
  sharpe: number;
  liquidReserve: number;
  liquidReservePct: number;
}

export function VaultMetrics({
  tvl,
  netApy,
  sharpe,
  liquidReserve,
  liquidReservePct,
}: VaultMetricsProps) {
  const metrics = [
    {
      label: "TOTAL VAULT AUM",
      value: formatCurrency(tvl),
      badge: "100% Backed",
      badgeColor: "text-blue-400 bg-blue-500/10 border-blue-500/20",
    },
    {
      label: "NET STRATEGY APY",
      value: formatPercent(netApy),
      badge: "Sharpe Weighted",
      badgeColor: "text-emerald-400 bg-emerald-500/10 border-emerald-500/20",
    },
    {
      label: "SHARPE RATIO",
      value: sharpe.toFixed(2),
      badge: "Rf: 4.5% Benchmark",
      badgeColor: "text-purple-400 bg-purple-500/10 border-purple-500/20",
    },
    {
      label: "LIQUID SAFE RESERVE",
      value: formatCurrency(liquidReserve),
      badge: `${liquidReservePct.toFixed(1)}% (Floor: 10%)`,
      badgeColor: "text-amber-400 bg-amber-500/10 border-amber-500/20",
    },
  ];

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
      {metrics.map((m, idx) => (
        <div
          key={idx}
          className="pro-panel rounded-xl p-4 border border-[#1a2233] flex flex-col justify-between"
        >
          <div className="flex items-center justify-between text-[11px] font-mono text-slate-400">
            <span>{m.label}</span>
            <span className={`text-[10px] px-1.5 py-0.2 rounded border font-mono ${m.badgeColor}`}>
              {m.badge}
            </span>
          </div>
          <div className="text-xl sm:text-2xl font-bold font-mono text-white tracking-tight mt-1.5">
            {m.value}
          </div>
        </div>
      ))}
    </div>
  );
}
