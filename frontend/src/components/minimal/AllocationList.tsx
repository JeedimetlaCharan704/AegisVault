import React, { useState } from "react";
import { CheckCircle2, AlertTriangle, Shield, ExternalLink, ChevronDown, ChevronUp, Lock } from "lucide-react";
import { Strategy } from "../../lib/simulation-engine";
import { formatCurrency } from "../../lib/utils";

interface AllocationListProps {
  strategies: Strategy[];
  liquidReserveUsd: number;
  liquidReservePct: number;
}

export function AllocationList({
  strategies,
  liquidReserveUsd,
  liquidReservePct,
}: AllocationListProps) {
  const [expandedId, setExpandedId] = useState<string | null>(null);

  const toggleExpand = (id: string) => {
    setExpandedId((prev) => (prev === id ? null : id));
  };

  return (
    <div className="card-minimal rounded-2xl p-6 sm:p-7 border border-white/[0.08] w-full">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-4">
        <div className="flex items-center gap-3">
          <h3 className="text-sm font-semibold text-white uppercase tracking-wider font-mono">
            Active Strategy Allocation & Yield Markets
          </h3>
          <span className="text-[11px] font-mono text-zinc-400 bg-zinc-900 px-2 py-0.5 rounded border border-white/[0.08]">
            ERC-4626 Controlled
          </span>
        </div>
        <div className="flex items-center gap-3 text-xs font-mono text-zinc-400">
          <span>Max Pool Cap: <strong className="text-zinc-200">40.0%</strong></span>
          <span>·</span>
          <span>Reserve Floor: <strong className="text-emerald-400">10.0%</strong></span>
        </div>
      </div>

      {/* Spacious Segmented Progress Bar */}
      <div className="w-full h-3 rounded-full bg-zinc-900 overflow-hidden flex mb-6 border border-white/[0.08]">
        <div
          className="bg-emerald-500 h-full transition-all duration-500"
          style={{ width: `${liquidReservePct}%` }}
          title={`Safe Cash Reserve: ${liquidReservePct.toFixed(1)}%`}
        />
        {strategies.map((s, idx) => {
          const colors = ["bg-blue-500", "bg-purple-500", "bg-indigo-400"];
          const isPaused = s.status === "PAUSED" || s.status === "COMPROMISED";
          return (
            <div
              key={s.id}
              className={`h-full transition-all duration-500 ${isPaused ? "bg-rose-500" : colors[idx % colors.length]}`}
              style={{ width: `${s.allocationPct}%` }}
              title={`${s.name}: ${s.allocationPct.toFixed(1)}%`}
            />
          );
        })}
      </div>

      {/* Spacious Tabular Rows */}
      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs font-mono">
          <thead>
            <tr className="border-b border-white/[0.06] text-zinc-400 text-[11px] uppercase tracking-wider">
              <th className="pb-3 font-medium">Market / Strategy</th>
              <th className="pb-3 text-right font-medium">Net APY</th>
              <th className="pb-3 text-right font-medium">Allocation ($)</th>
              <th className="pb-3 text-right font-medium">Weight (%)</th>
              <th className="pb-3 text-center font-medium">Risk Score</th>
              <th className="pb-3 text-center font-medium">Sentinel State</th>
              <th className="pb-3 text-center font-medium">Details</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-white/[0.06]">
            {/* Liquid Reserve Row */}
            <tr className="hover:bg-zinc-900/40 transition-colors">
              <td className="py-4 font-sans">
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 rounded-lg bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center text-emerald-400">
                    <Shield className="w-4 h-4" />
                  </div>
                  <div>
                    <span className="font-semibold text-white text-xs block">Liquid Safe Reserve</span>
                    <span className="text-[11px] text-zinc-400 font-mono">USDC Vault Cash Buffer (Instant Exit)</span>
                  </div>
                </div>
              </td>
              <td className="py-4 text-right text-zinc-500">0.00%</td>
              <td className="py-4 text-right font-semibold text-white">{formatCurrency(liquidReserveUsd)}</td>
              <td className="py-4 text-right text-emerald-400 font-bold">{liquidReservePct.toFixed(1)}%</td>
              <td className="py-4 text-center text-emerald-400">
                <span className="inline-flex items-center gap-1.5 text-xs font-semibold">
                  <CheckCircle2 className="w-3.5 h-3.5" /> 100/100
                </span>
              </td>
              <td className="py-4 text-center">
                <span className="px-2.5 py-1 rounded-md text-[11px] font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                  SECURE BUFFER
                </span>
              </td>
              <td className="py-4 text-center text-zinc-500 text-[11px]">
                Safe Base
              </td>
            </tr>

            {/* Strategies */}
            {strategies.map((strat) => {
              const isPaused = strat.status === "PAUSED" || strat.status === "COMPROMISED";
              const isExpanded = expandedId === strat.id;

              return (
                <React.Fragment key={strat.id}>
                  <tr
                    onClick={() => toggleExpand(strat.id)}
                    className={`hover:bg-zinc-900/50 transition-colors cursor-pointer ${
                      isPaused ? "bg-rose-950/20" : ""
                    }`}
                  >
                    <td className="py-4 font-sans">
                      <div className="flex items-center gap-3">
                        <div
                          className={`w-8 h-8 rounded-lg border flex items-center justify-center text-xs font-bold ${
                            isPaused
                              ? "bg-rose-500/10 border-rose-500/30 text-rose-400"
                              : "bg-zinc-800 border-zinc-700 text-zinc-200"
                          }`}
                        >
                          {strat.protocol.slice(0, 2).toUpperCase()}
                        </div>
                        <div>
                          <span className="font-semibold text-white text-xs block">
                            {strat.name}
                          </span>
                          <span className="text-[11px] text-zinc-400 font-mono">
                            {strat.protocol} · Base Sepolia
                          </span>
                        </div>
                      </div>
                    </td>
                    <td className="py-4 text-right font-semibold text-emerald-400">
                      {strat.apy.toFixed(2)}%
                    </td>
                    <td className="py-4 text-right font-semibold text-white">
                      {formatCurrency(strat.allocationUsd)}
                    </td>
                    <td className="py-4 text-right">
                      <span
                        className={
                          strat.allocationPct > 35
                            ? "text-amber-400 font-bold"
                            : "text-zinc-200"
                        }
                      >
                        {strat.allocationPct.toFixed(1)}%
                      </span>
                    </td>
                    <td className="py-4 text-center">
                      <span
                        className={`inline-flex items-center gap-1.5 font-semibold text-xs ${
                          strat.healthScore < 70
                            ? "text-rose-400 font-bold"
                            : "text-zinc-200"
                        }`}
                      >
                        {strat.healthScore < 70 && (
                          <AlertTriangle className="w-3.5 h-3.5 text-rose-400" />
                        )}
                        {strat.healthScore.toFixed(1)}/100
                      </span>
                    </td>
                    <td className="py-4 text-center">
                      {isPaused ? (
                        <span className="px-2.5 py-1 rounded-md text-[11px] font-bold bg-rose-500/15 text-rose-400 border border-rose-500/30">
                          ISOLATED · RECALLED
                        </span>
                      ) : (
                        <span className="px-2.5 py-1 rounded-md text-[11px] font-medium bg-zinc-800 text-zinc-300 border border-zinc-700">
                          ACTIVE
                        </span>
                      )}
                    </td>
                    <td className="py-4 text-center">
                      <button className="text-zinc-400 hover:text-white transition-colors p-1">
                        {isExpanded ? (
                          <ChevronUp className="w-4 h-4" />
                        ) : (
                          <ChevronDown className="w-4 h-4" />
                        )}
                      </button>
                    </td>
                  </tr>

                  {/* Expandable Deep Telemetry Drawer */}
                  {isExpanded && (
                    <tr className="bg-zinc-900/30">
                      <td colSpan={7} className="p-4 border-t border-b border-white/[0.04]">
                        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs font-mono">
                          <div className="p-3 rounded-lg bg-zinc-900/70 border border-white/[0.04]">
                            <span className="text-[10px] text-zinc-400 block mb-1">
                              Contract Cap Headroom
                            </span>
                            <span className="text-white font-bold block">
                              {(40.0 - strat.allocationPct).toFixed(1)}% remaining
                            </span>
                            <span className="text-[10px] text-zinc-400">
                              Limit: 40.0% ($600,000)
                            </span>
                          </div>

                          <div className="p-3 rounded-lg bg-zinc-900/70 border border-white/[0.04]">
                            <span className="text-[10px] text-zinc-400 block mb-1">
                              Protocol Volatility (30d)
                            </span>
                            <span className="text-zinc-200 font-bold block">
                              ±{strat.volatility.toFixed(1)}%
                            </span>
                            <span className="text-[10px] text-zinc-400">
                              Sharpe input factor
                            </span>
                          </div>

                          <div className="p-3 rounded-lg bg-zinc-900/70 border border-white/[0.04]">
                            <span className="text-[10px] text-zinc-400 block mb-1">
                              Anomaly Intercept Score
                            </span>
                            <span
                              className={`font-bold block ${
                                strat.anomalyScore > 0.5
                                  ? "text-rose-400"
                                  : "text-emerald-400"
                              }`}
                            >
                              {(strat.anomalyScore * 100).toFixed(0)} / 100
                            </span>
                            <span className="text-[10px] text-zinc-400">
                              Threshold trigger: 75
                            </span>
                          </div>

                          <div className="p-3 rounded-lg bg-zinc-900/70 border border-white/[0.04]">
                            <span className="text-[10px] text-zinc-400 block mb-1">
                              Security Verification
                            </span>
                            <span className="text-emerald-400 font-bold block flex items-center gap-1">
                              <Lock className="w-3 h-3" /> Audited
                            </span>
                            <span className="text-[10px] text-zinc-400">
                              Formal spec checked
                            </span>
                          </div>
                        </div>
                      </td>
                    </tr>
                  )}
                </React.Fragment>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
