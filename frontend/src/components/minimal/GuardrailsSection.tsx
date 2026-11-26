import React from "react";
import { Check, Zap, RefreshCw } from "lucide-react";
import { SpotlightCard } from "../magic/SpotlightCard";

interface GuardrailsSectionProps {
  threatLevel: "LOW" | "ELEVATED" | "CRITICAL";
  onTriggerAttack: () => void;
  onResetVault: () => void;
}

export function GuardrailsSection({
  threatLevel,
  onTriggerAttack,
  onResetVault,
}: GuardrailsSectionProps) {
  const isAttack = threatLevel === "CRITICAL";

  const invariants = [
    { title: "Max Pool Allocation", value: "≤ 40.0% of Vault TVL", formula: "Pool_i ≤ 0.40 * TVL" },
    { title: "Liquid Reserve Floor", value: "≥ 10.0% Safe Buffer", formula: "Reserve ≥ 0.10 * TVL" },
    { title: "Max Rebalance Slippage", value: "≤ 50 BPS (0.50%)", formula: "Slippage ≤ 0.50%" },
    { title: "Drawdown Circuit Breaker", value: "Auto-Pause on 5% Drop", formula: "Δ AUM < 5% / 1hr" },
  ];

  return (
    <SpotlightCard className="p-6 sm:p-7 w-full" spotlightColor="rgba(147, 51, 234, 0.1)">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-5">
        <div>
          <h3 className="text-sm font-semibold text-white uppercase tracking-wider font-mono">
            On-Chain Invariant Guardrails
          </h3>
          <p className="text-xs text-zinc-400 mt-1">
            Hard-coded Solidity rules enforced by <code>InvariantGuard.sol</code>. Off-chain agents cannot bypass these bounds.
          </p>
        </div>

        {/* Defense test trigger */}
        <div>
          {isAttack ? (
            <button
              onClick={onResetVault}
              className="inline-flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-mono font-bold bg-emerald-600 hover:bg-emerald-500 text-white transition-all shadow-md"
            >
              <RefreshCw className="w-3.5 h-3.5" />
              Reset Market State
            </button>
          ) : (
            <button
              onClick={onTriggerAttack}
              className="group relative inline-flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-mono font-bold border border-rose-500/40 bg-rose-950/30 hover:bg-rose-900/40 text-rose-300 hover:text-white transition-all shadow-sm overflow-hidden"
            >
              <Zap className="w-3.5 h-3.5 text-rose-400 fill-current animate-pulse" />
              <span>Test Defense: Simulate Exploit</span>
              {/* Subtle light sweep */}
              <div className="absolute inset-0 -translate-x-full group-hover:translate-x-full transition-transform duration-700 bg-gradient-to-r from-transparent via-rose-500/20 to-transparent pointer-events-none" />
            </button>
          )}
        </div>
      </div>

      {/* Exploit Alert Banner if Active */}
      {isAttack && (
        <div className="p-4 rounded-xl bg-rose-950/30 border border-rose-500/40 mb-5 text-xs font-mono animate-in fade-in duration-300">
          <div className="flex items-center gap-2 text-rose-300 font-semibold mb-1">
            <span className="w-2 h-2 rounded-full bg-rose-400 animate-ping" />
            Exploit Intercepted by Threat Sentinel
          </div>
          <p className="text-zinc-300 leading-relaxed text-xs">
            Anomalous borrow/swap pattern detected on Morpho Blue. Sentinel executed <code>emergencyDeRisk()</code>: 
            <strong className="text-white"> $450,000 recalled to safe vault reserve</strong>. Reserve elevated to 45.0%. Zero investor capital lost.
          </p>
        </div>
      )}

      {/* 4 Invariants Grid */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        {invariants.map((inv, idx) => (
          <div
            key={idx}
            className="p-4 rounded-xl bg-zinc-900/60 border border-white/[0.06] hover:border-white/[0.12] transition-colors flex flex-col justify-between"
          >
            <div>
              <div className="flex items-center justify-between text-xs mb-1.5">
                <span className="font-semibold text-zinc-200 font-sans">{inv.title}</span>
                <Check className="w-4 h-4 text-emerald-400" />
              </div>
              <span className="text-xs font-mono text-zinc-400 block">{inv.value}</span>
            </div>
            <div className="mt-3 pt-2 border-t border-white/[0.06] text-[10px] font-mono text-zinc-500">
              {inv.formula}
            </div>
          </div>
        ))}
      </div>
    </SpotlightCard>
  );
}
