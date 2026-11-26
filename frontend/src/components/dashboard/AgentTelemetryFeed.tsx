import React from "react";
import { Terminal } from "lucide-react";
import { TelemetryLog } from "../../lib/simulation-engine";

interface AgentTelemetryFeedProps {
  logs: TelemetryLog[];
}

export function AgentTelemetryFeed({ logs }: AgentTelemetryFeedProps) {
  const getBadgeClass = (agent: string) => {
    switch (agent) {
      case "SENTINEL":
        return "text-rose-400 bg-rose-500/10 border-rose-500/30";
      case "QUANT":
        return "text-purple-400 bg-purple-500/10 border-purple-500/30";
      case "AUDITOR":
        return "text-blue-400 bg-blue-500/10 border-blue-500/30";
      default:
        return "text-emerald-400 bg-emerald-500/10 border-emerald-500/30";
    }
  };

  return (
    <div className="zinc-card rounded-xl overflow-hidden border border-zinc-800 flex flex-col">
      <div className="px-4 py-2.5 border-b border-zinc-800 bg-zinc-900/60 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Terminal className="w-3.5 h-3.5 text-emerald-400" />
          <h4 className="text-xs font-bold text-white font-mono uppercase tracking-wider">
            Agent Audit Log
          </h4>
        </div>
        <span className="text-[10px] font-mono text-zinc-500">
          EIP-712 Signed Intents
        </span>
      </div>

      <div className="p-3 bg-zinc-950 overflow-y-auto max-h-[180px] space-y-2 font-mono text-[11px]">
        {logs.slice().reverse().map((log) => (
          <div
            key={log.id}
            className="p-2 rounded bg-zinc-900/50 border border-zinc-800/80 flex flex-col gap-1"
          >
            <div className="flex items-center justify-between text-[10px] text-zinc-400">
              <div className="flex items-center gap-1.5">
                <span className={`px-1.5 py-0.2 rounded border font-semibold ${getBadgeClass(log.agent)}`}>
                  {log.agent}
                </span>
                <span className="text-zinc-500">{log.timestamp}</span>
              </div>
              {log.txHash && <span className="text-blue-400">{log.txHash}</span>}
            </div>
            <p className={
              log.type === "CRITICAL"
                ? "text-rose-300 font-semibold"
                : log.type === "SUCCESS"
                ? "text-emerald-300"
                : "text-zinc-300"
            }>
              {log.message}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}
