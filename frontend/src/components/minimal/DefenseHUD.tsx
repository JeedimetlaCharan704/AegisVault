import React, { useEffect, useState } from "react";
import { ShieldCheck, Lock, AlertTriangle, ArrowRight, X } from "lucide-react";

interface DefenseHUDProps {
  isOpen: boolean;
  onClose: () => void;
}

export function DefenseHUD({ isOpen, onClose }: DefenseHUDProps) {
  const [step, setStep] = useState<number>(0);

  useEffect(() => {
    if (isOpen) {
      setStep(1);
      const t1 = setTimeout(() => setStep(2), 500);
      const t2 = setTimeout(() => setStep(3), 1100);
      const t3 = setTimeout(() => setStep(4), 1700);

      return () => {
        clearTimeout(t1);
        clearTimeout(t2);
        clearTimeout(t3);
      };
    } else {
      setStep(0);
    }
  }, [isOpen]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/85 backdrop-blur-md animate-in fade-in duration-200">
      <div className="card-minimal w-full max-w-lg rounded-2xl p-6 sm:p-8 border border-emerald-500/30 relative overflow-hidden shadow-2xl shadow-emerald-950/40">
        {/* Subtle Ambient Radial Glow */}
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-80 h-80 bg-emerald-500/10 rounded-full blur-3xl pointer-events-none" />

        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute top-4 right-4 p-1.5 rounded-lg text-zinc-400 hover:text-white hover:bg-white/5 transition-colors"
        >
          <X className="w-4 h-4" />
        </button>

        {/* Animated Cyber Shield & Shockwave Rings */}
        <div className="flex flex-col items-center justify-center pt-2 pb-6 text-center">
          <div className="relative w-20 h-20 flex items-center justify-center mb-5">
            {/* Shockwave Rings */}
            <div className="absolute inset-0 rounded-full border border-emerald-500/40 shield-pulse-ring pointer-events-none" />
            <div className="absolute inset-0 rounded-full border border-blue-500/30 shield-pulse-ring pointer-events-none [animation-delay:0.5s]" />
            <div className="absolute inset-0 rounded-full border border-emerald-400/20 shield-pulse-ring pointer-events-none [animation-delay:1s]" />

            {/* Central Glowing Shield Icon */}
            <div className="relative w-16 h-16 rounded-2xl bg-zinc-900 border border-emerald-500/40 flex items-center justify-center text-emerald-400 shadow-xl shadow-emerald-500/20">
              <ShieldCheck className="w-8 h-8" />
            </div>
          </div>

          <span className="text-[11px] font-mono font-semibold tracking-wider text-emerald-400 bg-emerald-500/10 px-2.5 py-1 rounded-full border border-emerald-500/20 uppercase mb-2">
            Sentinel Shield Protocol Engaged
          </span>

          <h3 className="text-xl font-bold text-white tracking-tight font-sans">
            Autonomous Exploit Interception
          </h3>
          <p className="text-xs text-zinc-400 mt-1 max-w-sm">
            Sub-block threat detection executed on-chain. Capital successfully evacuated before exploit completion.
          </p>
        </div>

        {/* Step-by-Step Live Execution Stream */}
        <div className="space-y-2.5 font-mono text-xs mb-6">
          <div className={`p-2.5 rounded-lg border transition-all duration-300 flex items-center justify-between ${
            step >= 1 ? "bg-amber-950/20 border-amber-500/30 text-amber-300" : "bg-zinc-900/30 border-white/[0.04] text-zinc-500"
          }`}>
            <span className="flex items-center gap-2">
              <span className="w-1.5 h-1.5 rounded-full bg-amber-400" />
              0ms: Flash-loan drain pattern flagged on Morpho
            </span>
            <span className="text-[10px] text-zinc-400">DETECTED</span>
          </div>

          <div className={`p-2.5 rounded-lg border transition-all duration-300 flex items-center justify-between ${
            step >= 2 ? "bg-blue-950/20 border-blue-500/30 text-blue-300" : "bg-zinc-900/30 border-white/[0.04] text-zinc-500"
          }`}>
            <span className="flex items-center gap-2">
              <span className="w-1.5 h-1.5 rounded-full bg-blue-400" />
              72ms: Sentinel broadcasts emergencyDeRisk()
            </span>
            <span className="text-[10px] text-zinc-400">SIGNATURE SIGNED</span>
          </div>

          <div className={`p-2.5 rounded-lg border transition-all duration-300 flex items-center justify-between ${
            step >= 3 ? "bg-emerald-950/30 border-emerald-500/40 text-emerald-300 font-semibold" : "bg-zinc-900/30 border-white/[0.04] text-zinc-500"
          }`}>
            <span className="flex items-center gap-2">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-ping" />
              180ms: $450,000 recalled to safe vault reserve
            </span>
            <span className="text-[10px] text-emerald-400">CONFIRMED</span>
          </div>

          <div className={`p-2.5 rounded-lg border transition-all duration-300 flex items-center justify-between ${
            step >= 4 ? "bg-zinc-900 border-zinc-700 text-white" : "bg-zinc-900/30 border-white/[0.04] text-zinc-500"
          }`}>
            <span className="flex items-center gap-2">
              <Lock className="w-3.5 h-3.5 text-emerald-400" />
              210ms: Vault sealed • Zero investor capital lost
            </span>
            <span className="text-[10px] text-emerald-400 font-bold">100% PROTECTED</span>
          </div>
        </div>

        {/* Dismiss Button */}
        <button
          onClick={onClose}
          className="w-full py-3 rounded-xl text-xs font-semibold bg-white hover:bg-zinc-200 text-black transition-colors font-sans flex items-center justify-center gap-2 shadow-lg"
        >
          <span>Return to Dashboard</span>
          <ArrowRight className="w-3.5 h-3.5" />
        </button>
      </div>
    </div>
  );
}
