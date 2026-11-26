import React from "react";
import { ShieldCheck, TrendingUp, DollarSign, Activity, AlertCircle } from "lucide-react";
import { formatCurrency, formatPercent } from "../../lib/utils";

interface HeroBannerProps {
  tvl: number;
  netApy: number;
  sharpe: number;
  liquidReserve: number;
  liquidReservePct: number;
  threatLevel: "LOW" | "ELEVATED" | "CRITICAL";
}

export function HeroBanner({
  tvl,
  netApy,
  sharpe,
  liquidReserve,
  liquidReservePct,
  threatLevel,
}: HeroBannerProps) {
  const isAttack = threatLevel === "CRITICAL";

  return (
    <div className="space-y-4">
      {/* Title & Context */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-1">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="text-[11px] font-mono px-2 py-0.5 rounded bg-blue-500/10 text-blue-400 border border-blue-500/20">
              Base Sepolia Testnet
            </span>
            <span className="text-[11px] font-mono text-zinc-500">
              Contract: 0x8920...43e7
            </span>
          </div>
          <h2 className="text-xl sm:text-2xl font-bold tracking-tight text-white font-sans">
            Autonomous Threat-Sentinel & Rebalancing Vault
          </h2>
          <p className="text-xs text-zinc-400 mt-0.5">
            Non-custodial ERC-4626 vault with autonomous off-chain threat monitoring and on-chain mathematical invariant circuit breakers.
          </p>
        </div>

        {/* Live Sentinel Status Pill */}
        <div className="shrink-0">
          <div
            className={`inline-flex items-center gap-2 px-3 py-1.5 rounded-lg border text-xs font-mono font-medium ${
              isAttack
                ? "bg-rose-950/40 text-rose-300 border-rose-500/40 animate-pulse"
                : "bg-emerald-950/30 text-emerald-300 border-emerald-500/30"
            }`}
          >
            <span
              className={`w-2 h-2 rounded-full ${
                isAttack ? "bg-rose-400 animate-ping" : "bg-emerald-400"
              }`}
            />
            <span>Sentinel Status: <strong className="uppercase">{threatLevel} THREAT</strong></span>
          </div>
        </div>
      </div>

      {/* Top 4 KPI Metric Tiles */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        <div className="zinc-card rounded-xl p-3.5 border border-zinc-800">
          <div className="flex items-center justify-between text-[11px] font-mono text-zinc-400">
            <span>TOTAL VAULT AUM</span>
            <span className="text-blue-400">100% Backed</span>
          </div>
          <div className="text-xl sm:text-2xl font-bold font-mono text-white tracking-tight mt-1">
            {formatCurrency(tvl)}
          </div>
          <span className="text-[10px] text-zinc-500 font-mono mt-0.5 block">
            USDC Collateral Pool
          </span>
        </div>

        <div className="zinc-card rounded-xl p-3.5 border border-zinc-800">
          <div className="flex items-center justify-between text-[11px] font-mono text-zinc-400">
            <span>NET STRATEGY APY</span>
            <span className="text-emerald-400">Sharpe-Weighted</span>
          </div>
          <div className="text-xl sm:text-2xl font-bold font-mono text-emerald-400 tracking-tight mt-1">
            {formatPercent(netApy)}
          </div>
          <span className="text-[10px] text-zinc-500 font-mono mt-0.5 block">
            Annualized Net Yield
          </span>
        </div>

        <div className="zinc-card rounded-xl p-3.5 border border-zinc-800">
          <div className="flex items-center justify-between text-[11px] font-mono text-zinc-400">
            <span>SHARPE RATIO</span>
            <span className="text-purple-400">Rf: 4.5%</span>
          </div>
          <div className="text-xl sm:text-2xl font-bold font-mono text-white tracking-tight mt-1">
            {sharpe.toFixed(2)}
          </div>
          <span className="text-[10px] text-zinc-500 font-mono mt-0.5 block">
            Risk-Adjusted Efficiency
          </span>
        </div>

        <div className="zinc-card rounded-xl p-3.5 border border-zinc-800">
          <div className="flex items-center justify-between text-[11px] font-mono text-zinc-400">
            <span>LIQUID SAFE RESERVE</span>
            <span className="text-amber-400">{liquidReservePct.toFixed(1)}%</span>
          </div>
          <div className="text-xl sm:text-2xl font-bold font-mono text-white tracking-tight mt-1">
            {formatCurrency(liquidReserve)}
          </div>
          <span className="text-[10px] text-zinc-500 font-mono mt-0.5 block">
            Unallocated Cash (Floor: 10%)
          </span>
        </div>
      </div>
    </div>
  );
}
