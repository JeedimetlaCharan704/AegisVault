import React from "react";
import { Radar, ShieldAlert, CheckCircle2 } from "lucide-react";
import { Strategy } from "../../lib/simulation-engine";

interface ThreatRadarProps {
  threatLevel: "LOW" | "ELEVATED" | "CRITICAL";
  strategies: Strategy[];
}

export function ThreatRadar({ threatLevel, strategies }: ThreatRadarProps) {
  const isAttack = threatLevel === "CRITICAL";

  return (
    <div className={`pro-panel rounded-xl p-4 border transition-colors ${
      isAttack ? "border-rose-500/50 bg-[#160c12]" : "border-[#1a2233]"
    }`}>
      <div className="flex items-center justify-between pb-3 border-b border-[#1a2233]">
        <div className="flex items-center gap-2">
          <Radar className={`w-4 h-4 ${isAttack ? "text-rose-400 animate-spin" : "text-emerald-400"}`} />
          <h4 className="text-xs font-bold text-white font-mono uppercase tracking-wider">
            Sentinel Threat Radar
          </h4>
        </div>
        <span className={`text-[10px] font-mono font-bold px-2 py-0.5 rounded border ${
          isAttack
            ? "bg-rose-500/10 text-rose-400 border-rose-500/30 animate-pulse"
            : "bg-emerald-500/10 text-emerald-400 border-emerald-500/20"
        }`}>
          {isAttack ? "ANOMALY CONFIRMED" : "MEMPOOL CLEAN"}
        </span>
      </div>

      <div className="flex items-center gap-4 py-3">
        {/* Radar Circular graphic */}
        <div className="relative w-24 h-24 rounded-full border border-[#1f2b42] flex items-center justify-center shrink-0">
          <div className="w-16 h-16 rounded-full border border-[#1a2438] flex items-center justify-center">
            <div className="w-8 h-8 rounded-full border border-[#161f30]" />
          </div>
          <div className={`absolute inset-0 rounded-full pointer-events-none ${
            isAttack ? "bg-rose-500/20 animate-pulse" : "radar-scanner opacity-50"
          }`} />

          {/* Dots */}
          <div className="absolute top-4 left-6 w-2 h-2 rounded-full bg-emerald-400" />
          {isAttack ? (
            <div className="absolute bottom-5 right-5 w-2.5 h-2.5 rounded-full bg-rose-500 animate-ping" />
          ) : (
            <div className="absolute bottom-5 right-5 w-2 h-2 rounded-full bg-blue-400" />
          )}
        </div>

        {/* Threat Diagnosis */}
        <div className="flex-1 text-xs font-mono">
          {isAttack ? (
            <div className="space-y-1 text-rose-300">
              <span className="font-bold flex items-center gap-1 text-rose-400 text-xs">
                <ShieldAlert className="w-3.5 h-3.5" /> Flash Loan Drain Flagged
              </span>
              <p className="text-[11px] text-rose-400/80 leading-relaxed">
                Morpho Blue health dropped to 32.0. Sentinel moved $450k to reserve.
              </p>
            </div>
          ) : (
            <div className="space-y-1 text-slate-400">
              <span className="font-semibold text-emerald-400 flex items-center gap-1 text-xs">
                <CheckCircle2 className="w-3.5 h-3.5" /> Sub-Block Consensus Active
              </span>
              <p className="text-[11px] text-slate-400 leading-relaxed">
                Scanning Pyth oracles, Aave, and Morpho borrow velocities.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
