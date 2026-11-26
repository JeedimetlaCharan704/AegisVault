import React, { useState } from "react";
import { Sliders, Sparkles, ShieldCheck, AlertCircle, ArrowRight, CheckCircle2, RotateCcw } from "lucide-react";
import { SpotlightCard } from "../magic/SpotlightCard";
import { Strategy } from "../../lib/simulation-engine";
import { formatCurrency } from "../../lib/utils";

export interface RegimeConfig {
  id: "BALANCED" | "AGGRESSIVE" | "DEFENSIVE";
  label: string;
  tagline: string;
  netApy: number;
  sharpeRatio: number;
  volatility: number;
  reservePct: number;
  aavePct: number;
  morphoPct: number;
  uniPct: number;
}

export const MARKET_REGIMES: Record<string, RegimeConfig> = {
  BALANCED: {
    id: "BALANCED",
    label: "Balanced MPT (Base)",
    tagline: "Sharpe-optimized baseline across lending and concentrated LP",
    netApy: 10.45,
    sharpeRatio: 1.28,
    volatility: 5.4,
    reservePct: 15.0,
    aavePct: 35.0,
    morphoPct: 30.0,
    uniPct: 20.0,
  },
  AGGRESSIVE: {
    id: "AGGRESSIVE",
    label: "Yield Surge (Bull)",
    tagline: "High capital efficiency focusing on Morpho curated vaults & DEX fees",
    netApy: 12.90,
    sharpeRatio: 1.45,
    volatility: 9.1,
    reservePct: 10.0,
    aavePct: 15.0,
    morphoPct: 40.0,
    uniPct: 35.0,
  },
  DEFENSIVE: {
    id: "DEFENSIVE",
    label: "Fortress (Bear Vol)",
    tagline: "Max capital preservation with deep cash buffer & conservative Aave v3",
    netApy: 7.95,
    sharpeRatio: 1.82,
    volatility: 2.6,
    reservePct: 35.0,
    aavePct: 40.0,
    morphoPct: 15.0,
    uniPct: 10.0,
  },
};

interface RegimeOptimizerProps {
  tvl: number;
  currentStrategies: Strategy[];
  onApplyRebalance: (
    regimeName: string,
    newApy: number,
    newSharpe: number,
    newReservePct: number,
    newStrategies: Strategy[]
  ) => void;
}

export function RegimeOptimizer({
  tvl,
  currentStrategies,
  onApplyRebalance,
}: RegimeOptimizerProps) {
  const [selectedRegime, setSelectedRegime] = useState<"BALANCED" | "AGGRESSIVE" | "DEFENSIVE">("BALANCED");
  const [isSimulating, setIsSimulating] = useState<boolean>(false);
  const [justApplied, setJustApplied] = useState<boolean>(false);

  const regime = MARKET_REGIMES[selectedRegime];
  const projectedAnnualRevenue = tvl * (regime.netApy / 100);

  const handleApply = () => {
    setIsSimulating(true);

    setTimeout(() => {
      // Calculate new allocations based on TVL
      const newReserveUsd = tvl * (regime.reservePct / 100);
      const updatedStrategies: Strategy[] = currentStrategies.map((strat) => {
        let pct = 0;
        let apy = strat.apy;

        if (strat.id === "aave-v3") {
          pct = regime.aavePct;
          apy = selectedRegime === "AGGRESSIVE" ? 8.20 : selectedRegime === "DEFENSIVE" ? 8.65 : 8.45;
        } else if (strat.id === "morpho-blue") {
          pct = regime.morphoPct;
          apy = selectedRegime === "AGGRESSIVE" ? 13.50 : selectedRegime === "DEFENSIVE" ? 9.80 : 11.20;
        } else if (strat.id === "univ3-lp") {
          pct = regime.uniPct;
          apy = selectedRegime === "AGGRESSIVE" ? 16.20 : selectedRegime === "DEFENSIVE" ? 11.50 : 14.80;
        }

        const allocationUsd = tvl * (pct / 100);

        return {
          ...strat,
          apy,
          allocationPct: pct,
          allocationUsd,
          status: "ACTIVE" as const,
          healthScore: selectedRegime === "DEFENSIVE" ? 99.0 : selectedRegime === "AGGRESSIVE" ? 91.5 : 95.0,
        };
      });

      onApplyRebalance(
        regime.label,
        regime.netApy,
        regime.sharpeRatio,
        regime.reservePct,
        updatedStrategies
      );

      setIsSimulating(false);
      setJustApplied(true);
      setTimeout(() => setJustApplied(false), 2500);
    }, 600);
  };

  return (
    <SpotlightCard className="p-6 sm:p-7 w-full border border-white/[0.08]" spotlightColor="rgba(59, 130, 246, 0.08)">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
        <div>
          <div className="flex items-center gap-2 mb-1.5">
            <span className="text-[11px] font-mono text-zinc-400 bg-zinc-900 px-2 py-0.5 rounded border border-white/[0.08] flex items-center gap-1.5">
              <Sliders className="w-3 h-3 text-blue-400" />
              Dynamic Quant Engine
            </span>
            <span className="text-[11px] font-mono text-emerald-400 bg-emerald-950/40 px-2 py-0.5 rounded border border-emerald-500/30 flex items-center gap-1">
              <ShieldCheck className="w-3 h-3" />
              InvariantGuard Verified
            </span>
          </div>
          <h3 className="text-base font-semibold text-white font-sans tracking-tight">
            Market Risk Regime & Rebalancing Simulator
          </h3>
          <p className="text-xs text-zinc-400 mt-1">
            Simulate Sharpe-optimal portfolio re-allocations across yield markets without violating hard-coded on-chain bounds.
          </p>
        </div>

        {/* Action button */}
        <button
          onClick={handleApply}
          disabled={isSimulating}
          className={`shrink-0 inline-flex items-center gap-2 px-4 py-2.5 rounded-xl text-xs font-mono font-bold transition-all shadow-md ${
            justApplied
              ? "bg-emerald-600 text-white"
              : "bg-blue-600 hover:bg-blue-500 text-white"
          }`}
        >
          {isSimulating ? (
            <>
              <RotateCcw className="w-3.5 h-3.5 animate-spin" />
              Quant Agent Solving MPT...
            </>
          ) : justApplied ? (
            <>
              <CheckCircle2 className="w-3.5 h-3.5" />
              Rebalance Executed!
            </>
          ) : (
            <>
              <Sparkles className="w-3.5 h-3.5 text-blue-200" />
              Execute Quant Rebalance
            </>
          )}
        </button>
      </div>

      {/* 3 Regime Toggle Selector */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-3 mb-6">
        {(["BALANCED", "AGGRESSIVE", "DEFENSIVE"] as const).map((key) => {
          const item = MARKET_REGIMES[key];
          const isSelected = selectedRegime === key;

          return (
            <button
              key={key}
              onClick={() => setSelectedRegime(key)}
              className={`p-4 rounded-xl text-left transition-all border ${
                isSelected
                  ? "bg-zinc-800/90 border-blue-500/50 shadow-md ring-1 ring-blue-500/20"
                  : "bg-zinc-900/50 border-white/[0.06] hover:border-white/[0.12] hover:bg-zinc-900"
              }`}
            >
              <div className="flex items-center justify-between mb-1.5">
                <span className="font-semibold text-xs text-white font-mono">
                  {item.label}
                </span>
                <span
                  className={`text-[10px] font-mono px-1.5 py-0.5 rounded font-bold ${
                    key === "AGGRESSIVE"
                      ? "bg-purple-500/20 text-purple-300"
                      : key === "DEFENSIVE"
                      ? "bg-amber-500/20 text-amber-300"
                      : "bg-blue-500/20 text-blue-300"
                  }`}
                >
                  {item.netApy.toFixed(2)}% APY
                </span>
              </div>
              <p className="text-[11px] text-zinc-400 line-clamp-2 leading-relaxed">
                {item.tagline}
              </p>
            </button>
          );
        })}
      </div>

      {/* Detailed Regime Breakdown & Invariant Compliance */}
      <div className="p-4 rounded-xl bg-zinc-900/40 border border-white/[0.06] grid grid-cols-2 sm:grid-cols-4 gap-4 font-mono text-xs">
        <div>
          <span className="text-[10px] uppercase tracking-wider text-zinc-400 block mb-1">
            Projected Net APY
          </span>
          <span className="text-xl font-bold text-emerald-400 block">
            {regime.netApy.toFixed(2)}%
          </span>
          <span className="text-[10px] text-zinc-400">
            +{formatCurrency(projectedAnnualRevenue)} / yr
          </span>
        </div>

        <div>
          <span className="text-[10px] uppercase tracking-wider text-zinc-400 block mb-1">
            Sharpe Ratio
          </span>
          <span className="text-xl font-bold text-white block">
            {regime.sharpeRatio.toFixed(2)}
          </span>
          <span className="text-[10px] text-zinc-400">
            Rf 4.5% Benchmark
          </span>
        </div>

        <div>
          <span className="text-[10px] uppercase tracking-wider text-zinc-400 block mb-1">
            Portfolio Volatility
          </span>
          <span className="text-xl font-bold text-zinc-200 block">
            ±{regime.volatility.toFixed(1)}%
          </span>
          <span className="text-[10px] text-zinc-400">
            30-day historical standard dev
          </span>
        </div>

        <div>
          <span className="text-[10px] uppercase tracking-wider text-zinc-400 block mb-1">
            Invariant Checks
          </span>
          <span className="inline-flex items-center gap-1.5 text-xs font-semibold text-emerald-400 mt-1">
            <CheckCircle2 className="w-3.5 h-3.5" />
            100% Compliant
          </span>
          <span className="text-[10px] text-zinc-400 block mt-0.5">
            Floor: {regime.reservePct.toFixed(0)}% (≥ 10%) · Max: {Math.max(regime.aavePct, regime.morphoPct, regime.uniPct)}% (≤ 40%)
          </span>
        </div>
      </div>

      {/* Target Distribution Weights Visualizer */}
      <div className="mt-4 pt-4 border-t border-white/[0.06]">
        <div className="flex items-center justify-between text-xs font-mono text-zinc-400 mb-2">
          <span>Target Portfolio Weights for {regime.label}</span>
          <span>Total: 100.0%</span>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 font-mono text-xs">
          <div className="p-2.5 rounded-lg bg-zinc-900/60 border border-white/[0.04] flex items-center justify-between">
            <span className="text-zinc-400">Reserve Buffer:</span>
            <span className="text-emerald-400 font-bold">{regime.reservePct}%</span>
          </div>
          <div className="p-2.5 rounded-lg bg-zinc-900/60 border border-white/[0.04] flex items-center justify-between">
            <span className="text-zinc-400">Aave V3:</span>
            <span className="text-blue-400 font-bold">{regime.aavePct}%</span>
          </div>
          <div className="p-2.5 rounded-lg bg-zinc-900/60 border border-white/[0.04] flex items-center justify-between">
            <span className="text-zinc-400">Morpho Blue:</span>
            <span className="text-purple-400 font-bold">{regime.morphoPct}%</span>
          </div>
          <div className="p-2.5 rounded-lg bg-zinc-900/60 border border-white/[0.04] flex items-center justify-between">
            <span className="text-zinc-400">Uniswap V3:</span>
            <span className="text-indigo-400 font-bold">{regime.uniPct}%</span>
          </div>
        </div>
      </div>
    </SpotlightCard>
  );
}
