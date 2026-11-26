import React from "react";
import { Layers, AlertTriangle, CheckCircle, Shield } from "lucide-react";
import { Card, CardHeader, CardTitle, CardContent } from "../ui/Card";
import { Badge } from "../ui/Badge";
import { Strategy } from "../../lib/simulation-engine";
import { formatCurrency } from "../../lib/utils";

interface StrategyBreakdownProps {
  strategies: Strategy[];
  liquidReserveUsd: number;
  liquidReservePct: number;
}

export function StrategyBreakdown({
  strategies,
  liquidReserveUsd,
  liquidReservePct,
}: StrategyBreakdownProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>
          <Layers className="w-4 h-4 text-blue-400" />
          Live Strategy & Liquidity Allocations
        </CardTitle>
        <Badge variant="outline" className="font-mono text-xs">
          ERC-4626 Controlled
        </Badge>
      </CardHeader>
      <CardContent className="space-y-4">
        {/* Unallocated Liquid Reserve */}
        <div className="p-3.5 rounded-xl bg-slate-900/60 border border-slate-800 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-lg bg-amber-500/10 border border-amber-500/20 flex items-center justify-center text-amber-400">
              <Shield className="w-4 h-4" />
            </div>
            <div>
              <h5 className="text-sm font-semibold text-white">Liquid Vault Reserve</h5>
              <p className="text-xs text-slate-400">Unallocated USDC buffer (Protective Capital)</p>
            </div>
          </div>
          <div className="text-right">
            <span className="text-sm font-bold text-white font-mono">
              {formatCurrency(liquidReserveUsd)}
            </span>
            <span className="block text-xs font-mono text-amber-400">
              {liquidReservePct.toFixed(1)}% (Floor: 10%)
            </span>
          </div>
        </div>

        {/* Strategies List */}
        {strategies.map((strat) => {
          const isCompromised = strat.status === "COMPROMISED" || strat.status === "PAUSED";
          return (
            <div
              key={strat.id}
              className={`p-3.5 rounded-xl border transition-all duration-300 ${
                isCompromised
                  ? "bg-rose-950/20 border-rose-500/30"
                  : "bg-slate-900/40 border-slate-800 hover:border-slate-700"
              }`}
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div
                    className={`w-9 h-9 rounded-lg border flex items-center justify-center font-bold text-xs ${
                      isCompromised
                        ? "bg-rose-500/10 border-rose-500/20 text-rose-400"
                        : "bg-blue-500/10 border-blue-500/20 text-blue-400"
                    }`}
                  >
                    {strat.protocol.slice(0, 2).toUpperCase()}
                  </div>
                  <div>
                    <div className="flex items-center gap-2">
                      <h5 className="text-sm font-semibold text-white">{strat.name}</h5>
                      <Badge
                        variant={isCompromised ? "danger" : "success"}
                        className="text-[10px] py-0 font-mono"
                      >
                        {isCompromised ? "ISOLATED" : "ACTIVE"}
                      </Badge>
                    </div>
                    <div className="flex items-center gap-3 text-xs text-slate-400 mt-0.5">
                      <span>APY: <strong className="text-emerald-400">{strat.apy}%</strong></span>
                      <span>Health: <strong className={strat.healthScore < 70 ? "text-rose-400" : "text-slate-300"}>{strat.healthScore}/100</strong></span>
                    </div>
                  </div>
                </div>

                <div className="text-right">
                  <span className="text-sm font-bold text-white font-mono">
                    {formatCurrency(strat.allocationUsd)}
                  </span>
                  <span className="block text-xs font-mono text-slate-400">
                    {strat.allocationPct.toFixed(1)}% (Cap: 40%)
                  </span>
                </div>
              </div>

              {/* Allocation bar */}
              <div className="w-full h-1.5 bg-slate-800 rounded-full mt-3 overflow-hidden">
                <div
                  className={`h-full rounded-full transition-all duration-500 ${
                    isCompromised ? "bg-rose-500" : "bg-blue-500"
                  }`}
                  style={{ width: `${strat.allocationPct}%` }}
                />
              </div>
            </div>
          );
        })}
      </CardContent>
    </Card>
  );
}
