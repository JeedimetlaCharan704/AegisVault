import React from "react";
import { Shield, Zap, RefreshCw, Wallet, ExternalLink, Terminal } from "lucide-react";

interface HeaderProps {
  activeTab: "overview" | "strategies" | "sentinel" | "invariants";
  setActiveTab: (tab: "overview" | "strategies" | "sentinel" | "invariants") => void;
  onTriggerAttack: () => void;
  onResetVault: () => void;
  onOpenInspect: () => void;
  threatLevel: "LOW" | "ELEVATED" | "CRITICAL";
  userBalance: number;
}

export function Header({
  activeTab,
  setActiveTab,
  onTriggerAttack,
  onResetVault,
  onOpenInspect,
  threatLevel,
  userBalance,
}: HeaderProps) {
  const isAttack = threatLevel === "CRITICAL";

  return (
    <header className="border-b border-zinc-800 bg-[#09090b]/90 backdrop-blur-md sticky top-0 z-40">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 h-14 flex items-center justify-between">
        {/* Brand */}
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-zinc-900 border border-zinc-800 flex items-center justify-center text-white">
            <Shield className="w-4 h-4 text-blue-400" />
          </div>
          <div className="flex items-center gap-2">
            <span className="font-bold text-sm tracking-tight text-white font-mono">
              Aegis<span className="text-blue-500">Vault</span>
            </span>
            <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800 text-zinc-400">
              ERC-4626
            </span>
          </div>
        </div>

        {/* Center Navigation Pills (Hackathon Standard) */}
        <nav className="hidden md:flex items-center bg-zinc-900/80 p-0.5 rounded-lg border border-zinc-800 text-xs font-medium">
          {(
            [
              { id: "overview", label: "Overview" },
              { id: "strategies", label: "Strategies" },
              { id: "sentinel", label: "Sentinel Brain" },
              { id: "invariants", label: "Guardrails" },
            ] as const
          ).map((t) => (
            <button
              key={t.id}
              onClick={() => setActiveTab(t.id)}
              className={`px-3 py-1 rounded-md transition-all ${
                activeTab === t.id
                  ? "bg-zinc-800 text-white shadow-sm font-semibold"
                  : "text-zinc-400 hover:text-zinc-200"
              }`}
            >
              {t.label}
            </button>
          ))}
        </nav>

        {/* Right Action Bar */}
        <div className="flex items-center gap-2.5">
          {/* Quick Attack Simulator Trigger */}
          {isAttack ? (
            <button
              onClick={onResetVault}
              className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-mono font-semibold bg-emerald-600 hover:bg-emerald-500 text-white transition-all shadow-sm"
            >
              <RefreshCw className="w-3.5 h-3.5" />
              Reset State
            </button>
          ) : (
            <button
              onClick={onTriggerAttack}
              className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-mono font-semibold bg-rose-600/90 hover:bg-rose-600 text-white transition-all shadow-sm shadow-rose-950"
            >
              <Zap className="w-3.5 h-3.5 fill-current" />
              Simulate Exploit
            </button>
          )}

          {/* Inspect Brain */}
          <button
            onClick={onOpenInspect}
            className="hidden sm:inline-flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg text-xs font-mono bg-zinc-900 hover:bg-zinc-800 border border-zinc-800 text-zinc-300 transition-all"
          >
            <Terminal className="w-3.5 h-3.5 text-blue-400" />
            Inspect
          </button>

          {/* Wallet Chip */}
          <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-mono bg-zinc-900 border border-zinc-800">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
            <span className="text-zinc-400">0x71C9...292e</span>
            <span className="text-zinc-600">|</span>
            <span className="text-zinc-200 font-bold">${userBalance.toLocaleString()}</span>
          </div>
        </div>
      </div>
    </header>
  );
}
