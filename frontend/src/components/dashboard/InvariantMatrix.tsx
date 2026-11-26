import React from "react";
import { Scale } from "lucide-react";

interface InvariantMatrixProps {
  circuitBreakerActive: boolean;
}

export function InvariantMatrix({ circuitBreakerActive }: InvariantMatrixProps) {
  const invariants = [
    {
      title: "Max Single-Pool Cap",
      rule: "Max 40.0% Allocation",
      formula: "Asset_i ≤ 0.40 * TVL",
      status: "PASS",
    },
    {
      title: "Liquid Reserve Floor",
      rule: "Min 10.0% Cash Buffer",
      formula: "Reserve ≥ 0.10 * TVL",
      status: "PASS",
    },
    {
      title: "Max Slippage Bounds",
      rule: "Revert if > 0.50% Slip",
      formula: "Slippage ≤ 50 BPS",
      status: "PASS",
    },
    {
      title: "Hourly Drawdown Breaker",
      rule: "Auto-Pause on 5% Drop",
      formula: "Δ AUM < 5% / 1hr",
      status: circuitBreakerActive ? "TRIPPED" : "HEALTHY",
    },
  ];

  return (
    <div className="zinc-card rounded-xl p-3.5 border border-zinc-800">
      <div className="flex items-center justify-between pb-2.5 border-b border-zinc-800 mb-2.5">
        <div className="flex items-center gap-2">
          <Scale className="w-3.5 h-3.5 text-purple-400" />
          <h4 className="text-xs font-bold text-white font-mono uppercase tracking-wider">
            On-Chain Invariant Guardrails
          </h4>
        </div>
        <span className="text-[10px] font-mono text-purple-400 bg-purple-500/10 px-1.5 py-0.2 rounded border border-purple-500/20">
          InvariantGuard.sol
        </span>
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
        {invariants.map((inv, idx) => (
          <div
            key={idx}
            className="p-2 rounded-lg bg-zinc-950 border border-zinc-800/80 flex flex-col justify-between"
          >
            <div className="flex items-center justify-between">
              <span className="text-[10px] font-semibold text-zinc-300 truncate">{inv.title}</span>
              <span className={`text-[9px] font-mono px-1.5 py-0.2 rounded font-bold ${
                inv.status === "TRIPPED"
                  ? "bg-rose-500/20 text-rose-400 border border-rose-500/40"
                  : "bg-emerald-500/10 text-emerald-400 border border-emerald-500/20"
              }`}>
                {inv.status}
              </span>
            </div>
            <div className="mt-1 text-[10px] font-mono text-zinc-500">
              {inv.formula}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
