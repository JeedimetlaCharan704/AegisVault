import React from "react";
import { ShieldCheck, Cpu, Database, CheckCircle2, Lock } from "lucide-react";
import { cn } from "../../lib/utils";

interface AnimatedBeamProps {
  isDeRisking?: boolean;
}

export function AnimatedPipeline({ isDeRisking = false }: AnimatedBeamProps) {
  const steps = [
    {
      id: "data",
      label: "Mempool / Pyth Feed",
      icon: Database,
      color: "text-slate-400 border-slate-700 bg-slate-900/60",
    },
    {
      id: "sentinel",
      label: "Threat Sentinel",
      icon: isDeRisking ? ShieldCheck : ShieldCheck,
      color: isDeRisking
        ? "text-rose-400 border-rose-500 bg-rose-950/40 animate-bounce"
        : "text-emerald-400 border-emerald-500/50 bg-emerald-950/30",
    },
    {
      id: "quant",
      label: "Quant Optimizer",
      icon: Cpu,
      color: "text-indigo-400 border-indigo-500/50 bg-indigo-950/30",
    },
    {
      id: "auditor",
      label: "Invariant Auditor",
      icon: CheckCircle2,
      color: "text-blue-400 border-blue-500/50 bg-blue-950/30",
    },
    {
      id: "vault",
      label: "AegisVault (ERC-4626)",
      icon: Lock,
      color: "text-amber-400 border-amber-500/50 bg-amber-950/30",
    },
  ];

  return (
    <div className="w-full py-4 relative">
      <div className="flex flex-col md:flex-row items-center justify-between gap-3 relative z-10">
        {steps.map((step, idx) => {
          const Icon = step.icon;
          return (
            <React.Fragment key={step.id}>
              <div className="flex flex-col items-center gap-2 group cursor-pointer">
                <div
                  className={cn(
                    "w-12 h-12 rounded-xl border flex items-center justify-center transition-all duration-300 shadow-lg",
                    step.color
                  )}
                >
                  <Icon className="w-5 h-5" />
                </div>
                <span className="text-xs font-medium text-slate-300 tracking-wide text-center">
                  {step.label}
                </span>
              </div>

              {idx < steps.length - 1 && (
                <div className="hidden md:flex flex-1 items-center px-2">
                  <div className="h-0.5 w-full bg-slate-800 relative overflow-hidden">
                    <div
                      className={cn(
                        "absolute top-0 bottom-0 left-0 w-1/3 bg-gradient-to-r transition-all duration-1000",
                        isDeRisking
                          ? "from-transparent via-rose-500 to-transparent animate-pulse w-full"
                          : "from-transparent via-blue-500 to-transparent animate-pulse"
                      )}
                    />
                  </div>
                </div>
              )}
            </React.Fragment>
          );
        })}
      </div>
    </div>
  );
}
