import React, { useState } from "react";
import { NumberTicker } from "../magic/NumberTicker";
import { SpotlightCard } from "../magic/SpotlightCard";
import { Copy, Check, ShieldCheck, ExternalLink } from "lucide-react";

interface VaultSummaryProps {
  tvl: number;
  netApy: number;
  sharpeRatio: number;
  liquidReserve: number;
  liquidReservePct: number;
  isAttackActive: boolean;
}

export function VaultSummary({
  tvl,
  netApy,
  sharpeRatio,
  liquidReserve,
  liquidReservePct,
  isAttackActive,
}: VaultSummaryProps) {
  const [copied, setCopied] = useState(false);
  const contractAddress = "0x89209581A7bF892c23F1E7b4C198F908381243e7";

  const handleCopy = () => {
    navigator.clipboard.writeText(contractAddress);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="pt-4 pb-2">
      {/* Title & Top Info Header */}
      <div className="flex flex-col lg:flex-row lg:items-end justify-between gap-6 pb-6 border-b border-white/[0.08]">
        <div className="max-w-2xl relative">
          <div className="flex flex-wrap items-center gap-2.5 mb-2.5">
            <span className="text-[11px] font-mono text-zinc-400 bg-zinc-900/90 px-2.5 py-1 rounded-md border border-white/[0.08] flex items-center gap-1.5">
              <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
              ERC-4626 Tokenized Vault
            </span>
            {isAttackActive ? (
              <span className="text-[11px] font-mono text-rose-300 bg-rose-950/40 px-2.5 py-1 rounded-md border border-rose-500/40 animate-pulse">
                Defense Active · Anomaly Isolated
              </span>
            ) : (
              <span className="text-[11px] font-mono text-emerald-300 bg-emerald-950/40 px-2.5 py-1 rounded-md border border-emerald-500/30">
                Sentinel Guard Active
              </span>
            )}
            
            {/* Quick Copy Contract Address */}
            <button
              onClick={handleCopy}
              className="text-[11px] font-mono text-zinc-400 hover:text-white bg-zinc-900/80 hover:bg-zinc-800 px-2.5 py-1 rounded-md border border-white/[0.08] flex items-center gap-1.5 transition-colors"
              title="Click to copy contract address"
            >
              {copied ? (
                <>
                  <Check className="w-3 h-3 text-emerald-400" />
                  <span className="text-emerald-400">Copied!</span>
                </>
              ) : (
                <>
                  <Copy className="w-3 h-3 text-zinc-500" />
                  <span>0x8920...43e7</span>
                </>
              )}
            </button>

            <span className="text-[11px] font-mono text-zinc-500 px-2 py-0.5 rounded bg-zinc-900/40 border border-white/[0.04]">
              Base Sepolia (84532)
            </span>
          </div>

          <h1 className="text-3xl sm:text-4xl font-semibold tracking-tight text-white font-sans">
            Aegis USDC Yield Vault
          </h1>
          <p className="text-sm text-zinc-400 mt-2 leading-relaxed">
            Autonomous multi-market liquidity allocation protected by off-chain threat sentinels and on-chain invariant circuit breakers.
          </p>
        </div>

        {/* 4 Spotlight Metric Cards (Clean minimal without blue border beam or blue line) */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 shrink-0 font-mono">
          <SpotlightCard className="p-4 sm:p-5" spotlightColor="rgba(255, 255, 255, 0.06)">
            <div className="text-[11px] text-zinc-400 uppercase tracking-wider">
              Total Assets (TVL)
            </div>
            <div className="text-2xl sm:text-3xl font-semibold text-white tracking-tight mt-1">
              <NumberTicker value={tvl} prefix="$" />
            </div>
            <span className="text-[10px] text-zinc-500 block mt-1">
              100% Backed Reserves
            </span>
          </SpotlightCard>

          <SpotlightCard className="p-4 sm:p-5" spotlightColor="rgba(16, 185, 129, 0.12)">
            <div className="text-[11px] text-zinc-400 uppercase tracking-wider">
              Net Strategy APY
            </div>
            <div className="text-2xl sm:text-3xl font-semibold text-emerald-400 tracking-tight mt-1">
              <NumberTicker value={netApy} suffix="%" decimals={2} />
            </div>
            <span className="text-[10px] text-zinc-500 block mt-1">
              Sharpe-Weighted Yield
            </span>
          </SpotlightCard>

          <SpotlightCard className="p-4 sm:p-5" spotlightColor="rgba(147, 51, 234, 0.12)">
            <div className="text-[11px] text-zinc-400 uppercase tracking-wider">
              Sharpe Ratio
            </div>
            <div className="text-2xl sm:text-3xl font-semibold text-white tracking-tight mt-1">
              <NumberTicker value={sharpeRatio} decimals={2} />
            </div>
            <span className="text-[10px] text-zinc-500 block mt-1">
              Rf: 4.5% Benchmark
            </span>
          </SpotlightCard>

          <SpotlightCard className="p-4 sm:p-5" spotlightColor="rgba(245, 158, 11, 0.12)">
            <div className="text-[11px] text-zinc-400 uppercase tracking-wider">
              Safe Cash Reserve
            </div>
            <div className="text-2xl sm:text-3xl font-semibold text-amber-400 tracking-tight mt-1">
              <NumberTicker value={liquidReservePct} suffix="%" decimals={1} />
            </div>
            <span className="text-[10px] text-zinc-500 block mt-1">
              Floor Requirement: 10%
            </span>
          </SpotlightCard>
        </div>
      </div>
    </div>
  );
}
