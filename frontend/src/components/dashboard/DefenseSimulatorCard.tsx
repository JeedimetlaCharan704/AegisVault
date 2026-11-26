import React from "react";
import { ShieldCheck, Zap, AlertTriangle, CheckCircle2, ArrowRight, RefreshCw, Cpu, Database, Lock } from "lucide-react";

interface DefenseSimulatorProps {
  threatLevel: "LOW" | "ELEVATED" | "CRITICAL";
  onTriggerAttack: () => void;
  onResetVault: () => void;
}

export function DefenseSimulatorCard({
  threatLevel,
  onTriggerAttack,
  onResetVault,
}: DefenseSimulatorProps) {
  const isAttack = threatLevel === "CRITICAL";

  return (
    <div
      className={`zinc-card rounded-xl p-4 border transition-all ${
        isAttack
          ? "border-rose-500/50 bg-[#160b10] shadow-xl shadow-rose-950/20"
          : "border-zinc-800"
      }`}
    >
      <div className="flex items-center justify-between pb-3 border-b border-zinc-800">
        <div className="flex items-center gap-2">
          <ShieldCheck className={`w-4 h-4 ${isAttack ? "text-rose-400" : "text-emerald-400"}`} />
          <h3 className="text-xs font-bold font-mono text-white uppercase tracking-wider">
            Autonomous Multi-Agent Defense Engine
          </h3>
        </div>
        <span
          className={`text-[10px] font-mono px-2 py-0.5 rounded border font-semibold ${
            isAttack
              ? "bg-rose-500/10 text-rose-400 border-rose-500/30"
              : "bg-emerald-500/10 text-emerald-400 border-emerald-500/20"
          }`}
        >
          {isAttack ? "ATTACK DEFENDED • RECALL EXECUTED" : "CONSENSUS ACTIVE • CLEAN"}
        </span>
      </div>

      {/* 3 Agent Pipeline Chips */}
      <div className="grid grid-cols-3 gap-2 my-3">
        <div className="p-2.5 rounded-lg bg-zinc-900 border border-zinc-800 flex flex-col items-center text-center">
          <span className="text-[10px] font-mono text-zinc-400 uppercase">1. Sentinel Agent</span>
          <span className={`text-xs font-bold font-mono mt-0.5 ${isAttack ? "text-rose-400" : "text-emerald-400"}`}>
            {isAttack ? "DRAIN INTERCEPTED" : "MEMPOOL CLEAN"}
          </span>
        </div>

        <div className="p-2.5 rounded-lg bg-zinc-900 border border-zinc-800 flex flex-col items-center text-center">
          <span className="text-[10px] font-mono text-zinc-400 uppercase">2. Quant Optimizer</span>
          <span className="text-xs font-bold font-mono mt-0.5 text-purple-400">
            {isAttack ? "DEFENSIVE RECUT" : "SHARPE: 1.28"}
          </span>
        </div>

        <div className="p-2.5 rounded-lg bg-zinc-900 border border-zinc-800 flex flex-col items-center text-center">
          <span className="text-[10px] font-mono text-zinc-400 uppercase">3. Invariant Auditor</span>
          <span className="text-xs font-bold font-mono mt-0.5 text-blue-400">
            {isAttack ? "RESERVE ELEVATED 45%" : "CAPS VERIFIED"}
          </span>
        </div>
      </div>

      {/* Live Feedback / Exploit Details */}
      {isAttack ? (
        <div className="p-3 rounded-lg bg-rose-950/30 border border-rose-500/30 text-xs font-mono space-y-1.5 mb-3">
          <div className="flex items-center gap-1.5 text-rose-300 font-bold">
            <AlertTriangle className="w-4 h-4 text-rose-400 shrink-0" />
            <span>Attack Scenario: Morpho Blue Flash Loan Liquidity Drain</span>
          </div>
          <p className="text-[11px] text-rose-400/80 leading-relaxed">
            Sentinel detected anomalous borrowing velocity within 180ms. Triggered <code>emergencyDeRisk()</code>: 
            <strong> $450,000 recalled to vault reserve</strong>. Target isolated. Zero capital lost.
          </p>
        </div>
      ) : (
        <div className="p-2.5 rounded-lg bg-zinc-900/60 border border-zinc-800/80 text-xs font-mono text-zinc-400 flex items-center justify-between mb-3">
          <span className="flex items-center gap-1.5">
            <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
            Sub-block oracle checks running. All 3 yield pools healthy.
          </span>
          <span className="text-[11px] text-zinc-500">Latency: 42ms</span>
        </div>
      )}

      {/* Action Buttons */}
      <div className="flex items-center gap-2">
        {isAttack ? (
          <button
            onClick={onResetVault}
            className="w-full py-2 px-3 rounded-lg text-xs font-mono font-bold bg-emerald-600 hover:bg-emerald-500 text-white flex items-center justify-center gap-2 transition-all"
          >
            <RefreshCw className="w-3.5 h-3.5" />
            Reset Market to Normal State
          </button>
        ) : (
          <button
            onClick={onTriggerAttack}
            className="w-full py-2.5 px-3 rounded-lg text-xs font-mono font-bold bg-rose-600 hover:bg-rose-500 text-white flex items-center justify-center gap-2 transition-all shadow-md shadow-rose-950"
          >
            <Zap className="w-3.5 h-3.5 fill-current" />
            Simulate Flash Loan Exploit Scenario (Test Defense)
          </button>
        )}
      </div>
    </div>
  );
}
