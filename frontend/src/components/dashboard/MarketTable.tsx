import React from "react";
import { Shield, AlertTriangle, CheckCircle2 } from "lucide-react";
import { Strategy } from "../../lib/simulation-engine";
import { formatCurrency } from "../../lib/utils";

interface MarketTableProps {
  strategies: Strategy[];
  liquidReserveUsd: number;
  liquidReservePct: number;
}

export function MarketTable({
  strategies,
  liquidReserveUsd,
  liquidReservePct,
}: MarketTableProps) {
  return (
    <div className="zinc-card rounded-xl overflow-hidden border border-zinc-800">
      <div className="px-4 py-3 border-b border-zinc-800 flex items-center justify-between bg-zinc-900/60">
        <div className="flex items-center gap-2">
          <h3 className="text-xs font-bold font-mono text-white uppercase tracking-wider">
            Strategy Allocations & Yield Pools
          </h3>
          <span className="text-[10px] font-mono text-zinc-400 bg-zinc-800 px-1.5 py-0.2 rounded border border-zinc-700">
            ERC-4626 Controlled
          </span>
        </div>
        <span className="text-[11px] text-zinc-400 font-mono">
          Single-Pool Cap: <strong className="text-zinc-200">40.0%</strong>
        </span>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs font-mono">
          <thead>
            <tr className="border-b border-zinc-800 text-zinc-400 text-[10px] uppercase tracking-wider bg-zinc-900/30">
              <th className="py-2.5 px-4 font-medium">Market / Strategy</th>
              <th className="py-2.5 px-4 font-medium text-right">Net APY</th>
              <th className="py-2.5 px-4 font-medium text-right">Allocation</th>
              <th className="py-2.5 px-4 font-medium text-right">Weight (%)</th>
              <th className="py-2.5 px-4 font-medium text-center">Health</th>
              <th className="py-2.5 px-4 font-medium text-center">Sentinel Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-zinc-800/80">
            {/* Liquid Vault Reserve Row */}
            <tr className="hover:bg-zinc-800/30 transition-colors">
              <td className="py-2.5 px-4">
                <div className="flex items-center gap-2">
                  <div className="w-6 h-6 rounded bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center text-emerald-400">
                    <Shield className="w-3 h-3" />
                  </div>
                  <div>
                    <span className="font-semibold text-white block text-xs">Liquid Safe Reserve</span>
                    <span className="text-[10px] text-zinc-500">USDC Cash Buffer (Floor: 10%)</span>
                  </div>
                </div>
              </td>
              <td className="py-2.5 px-4 text-right text-zinc-500 font-mono">0.00%</td>
              <td className="py-2.5 px-4 text-right font-bold text-white font-mono">
                {formatCurrency(liquidReserveUsd)}
              </td>
              <td className="py-2.5 px-4 text-right text-emerald-400 font-bold">
                {liquidReservePct.toFixed(1)}%
              </td>
              <td className="py-2.5 px-4 text-center">
                <span className="inline-flex items-center gap-1 text-[11px] text-emerald-400">
                  <CheckCircle2 className="w-3 h-3" /> 100/100
                </span>
              </td>
              <td className="py-2.5 px-4 text-center">
                <span className="px-2 py-0.5 rounded text-[10px] font-medium bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                  SECURE BUFFER
                </span>
              </td>
            </tr>

            {/* Individual Strategies */}
            {strategies.map((strat) => {
              const isPaused = strat.status === "PAUSED" || strat.status === "COMPROMISED";
              return (
                <tr
                  key={strat.id}
                  className={`hover:bg-zinc-800/30 transition-colors ${
                    isPaused ? "bg-rose-950/20" : ""
                  }`}
                >
                  <td className="py-2.5 px-4">
                    <div className="flex items-center gap-2">
                      <div
                        className={`w-6 h-6 rounded border flex items-center justify-center text-[10px] font-bold ${
                          isPaused
                            ? "bg-rose-500/10 border-rose-500/30 text-rose-400"
                            : "bg-blue-500/10 border-blue-500/20 text-blue-400"
                        }`}
                      >
                        {strat.protocol.slice(0, 2).toUpperCase()}
                      </div>
                      <div>
                        <span className="font-semibold text-white block text-xs">
                          {strat.name}
                        </span>
                        <span className="text-[10px] text-zinc-500">
                          {strat.protocol} • Base Sepolia
                        </span>
                      </div>
                    </div>
                  </td>

                  <td className="py-2.5 px-4 text-right font-bold font-mono text-emerald-400">
                    {strat.apy.toFixed(2)}%
                  </td>

                  <td className="py-2.5 px-4 text-right font-bold text-white font-mono">
                    {formatCurrency(strat.allocationUsd)}
                  </td>

                  <td className="py-2.5 px-4 text-right">
                    <span className={strat.allocationPct > 35 ? "text-amber-400 font-bold" : "text-zinc-300"}>
                      {strat.allocationPct.toFixed(1)}%
                    </span>
                  </td>

                  <td className="py-2.5 px-4 text-center">
                    <span
                      className={`inline-flex items-center gap-1 font-semibold ${
                        strat.healthScore < 70 ? "text-rose-400" : "text-zinc-300"
                      }`}
                    >
                      {strat.healthScore < 70 && <AlertTriangle className="w-3 h-3 text-rose-400" />}
                      {strat.healthScore.toFixed(1)}/100
                    </span>
                  </td>

                  <td className="py-2.5 px-4 text-center">
                    {isPaused ? (
                      <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-rose-500/15 text-rose-400 border border-rose-500/30">
                        🚨 ISOLATED / RECALLED
                      </span>
                    ) : (
                      <span className="px-2 py-0.5 rounded text-[10px] font-medium bg-blue-500/10 text-blue-400 border border-blue-500/20">
                        ACTIVE
                      </span>
                    )}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
