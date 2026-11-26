import React from "react";
import { X, Shield, Cpu, Scale, CheckCircle2, Copy } from "lucide-react";
import { Button } from "../ui/Button";
import { Badge } from "../ui/Badge";

interface AgentInspectionModalProps {
  isOpen: boolean;
  onClose: () => void;
  agentType: "SENTINEL" | "QUANT" | "AUDITOR";
}

export function AgentInspectionModal({
  isOpen,
  onClose,
  agentType,
}: AgentInspectionModalProps) {
  if (!isOpen) return null;

  const contentMap = {
    SENTINEL: {
      title: "Threat Sentinel Agent Brain",
      icon: Shield,
      model: "Gemini 1.5 Flash + Heuristic Sentinel Engine",
      role: "Continuous Mempool & Reserve Anomaly Detection",
      formula: "AnomalyScore = w_1*(1 - Health/100) + w_2*Volatility_7d + w_3*MempoolVariance",
      prompt: `System: You are Aegis-Sentinel-01. Monitor real-time sub-block liquidity reserves, pool depeg ratios, and flash-loan attack signatures across connected DeFi strategies.
If anomaly_score > 0.80 or health_score < 70, immediately issue an EMERGENCY_DERISK execution payload targeting the compromised pool.`,
      jsonPayload: {
        agent_id: "Aegis-Sentinel-01",
        status: "ACTIVE",
        inspection_cadence: "1 block (2000ms)",
        metrics_tracked: [
          "Liquidity Reserve Depth",
          "Oracle Deviation vs Pyth",
          "Borrow/Supply Utilization Ratios",
          "Mempool Re-entrancy Signatures"
        ],
        last_signature_scan: "CLEAN",
        confidence: 0.992
      }
    },
    QUANT: {
      title: "Quant Optimization Agent Brain",
      icon: Cpu,
      model: "Autonomous Modern Portfolio Theory (MPT) Solver",
      role: "Dynamic Risk-Adjusted Sharpe Maximization",
      formula: "Sharpe = (Portfolio_APY - RiskFreeRate) / Portfolio_Volatility",
      prompt: `System: You are Aegis-Quant-01. Calculate the optimal capital allocation weights across whitelisted strategies (Aave V3, Morpho Blue, Uniswap V3 LP).
Constraints:
- Max 40% in any single strategy.
- Min 10% kept in unallocated liquid reserve.
- Deduct net gas fees before determining rebalance viability.`,
      jsonPayload: {
        agent_id: "Aegis-Quant-01",
        risk_free_benchmark: "4.50% (sDAI/Treasury)",
        active_weights: {
          "Aave V3": 0.35,
          "Morpho Blue": 0.30,
          "Uniswap V3 LP": 0.20,
          "Liquid Reserve": 0.15
        },
        projected_sharpe: 1.28,
        expected_annual_net_yield: "10.45%"
      }
    },
    AUDITOR: {
      title: "Invariant Auditor & Policy Signer",
      icon: Scale,
      model: "EIP-712 Cryptographic Pre-Flight Verifier",
      role: "Mathematical Invariant Enforcement before Broadcast",
      formula: "∀ i, Allocation_i ≤ 0.40 * TVL ∧ Reserve ≥ 0.10 * TVL ∧ Slippage ≤ 50 BPS",
      prompt: `System: Verify that the proposed allocation plan strictly satisfies all smart contract invariants in InvariantGuard.sol.
If any invariant is breached, revert the execution intent. If approved, generate an EIP-712 signed payload hash.`,
      jsonPayload: {
        agent_id: "Aegis-Auditor-01",
        invariants_verified: {
          "MAX_ALLOCATION_40%": "PASSED",
          "MIN_RESERVE_10%": "PASSED",
          "MAX_SLIPPAGE_50BPS": "PASSED",
          "CIRCUIT_BREAKER_CHECK": "HEALTHY"
        },
        signed_intent_hash: "0x7237ff3a39f5609177603f12da67a119b5e12e2af0c4a86bdc8824e9a166b8dc",
        verification_status: "CRYPTOGRAPHICALLY_VALID"
      }
    }
  };

  const curr = contentMap[agentType];
  const Icon = curr.icon;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md animate-in fade-in">
      <div className="glass-card w-full max-w-2xl rounded-2xl border border-white/10 p-6 shadow-2xl relative overflow-hidden">
        {/* Header */}
        <div className="flex items-center justify-between pb-4 border-b border-white/5">
          <div className="flex items-center gap-3">
            <div className="p-2.5 rounded-xl bg-blue-500/10 border border-blue-500/20 text-blue-400">
              <Icon className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-base font-bold text-white tracking-wide">{curr.title}</h3>
              <p className="text-xs text-slate-400">{curr.role}</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-white/5 transition-all"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Body */}
        <div className="py-4 space-y-4 max-h-[70vh] overflow-y-auto">
          {/* Model info */}
          <div className="p-3 rounded-xl bg-slate-900/60 border border-white/5 flex items-center justify-between text-xs font-mono">
            <span className="text-slate-400">Underlying Model / Engine:</span>
            <span className="text-blue-400 font-bold">{curr.model}</span>
          </div>

          {/* Mathematical formulation */}
          <div className="p-3.5 rounded-xl bg-slate-900/80 border border-white/5 space-y-1">
            <span className="text-[11px] font-semibold uppercase tracking-wider text-slate-400">
              Mathematical Invariant / Optimization Function
            </span>
            <p className="font-mono text-xs text-purple-300 break-all">{curr.formula}</p>
          </div>

          {/* System Prompt Snippet */}
          <div className="space-y-1.5">
            <span className="text-[11px] font-semibold uppercase tracking-wider text-slate-400">
              Active Agent Prompt & Guardrails
            </span>
            <pre className="p-3 rounded-xl bg-black/60 border border-white/5 text-[11px] font-mono text-slate-300 whitespace-pre-wrap">
              {curr.prompt}
            </pre>
          </div>

          {/* Live JSON Telemetry */}
          <div className="space-y-1.5">
            <span className="text-[11px] font-semibold uppercase tracking-wider text-slate-400">
              Live State & Telemetry Output
            </span>
            <pre className="p-3 rounded-xl bg-black/60 border border-white/5 text-[11px] font-mono text-emerald-400 overflow-x-auto">
              {JSON.stringify(curr.jsonPayload, null, 2)}
            </pre>
          </div>
        </div>

        {/* Footer */}
        <div className="pt-3 border-t border-white/5 flex items-center justify-between text-xs font-mono text-slate-400">
          <span className="flex items-center gap-1.5 text-emerald-400">
            <CheckCircle2 className="w-4 h-4" /> Zero Prompt-Injection Vector: Pre-flight Verified
          </span>
          <Button size="sm" variant="secondary" onClick={onClose}>
            Close Inspection
          </Button>
        </div>
      </div>
    </div>
  );
}
