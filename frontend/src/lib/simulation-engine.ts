export interface Strategy {
  id: string;
  name: string;
  protocol: string;
  apy: number;
  allocationUsd: number;
  allocationPct: number;
  healthScore: number; // 0 - 100
  volatility: number;  // %
  status: "ACTIVE" | "COMPROMISED" | "PAUSED";
  anomalyScore: number;
}

export interface TelemetryLog {
  id: string;
  timestamp: string;
  agent: "SENTINEL" | "QUANT" | "AUDITOR" | "SYSTEM";
  type: "INFO" | "WARNING" | "CRITICAL" | "SUCCESS";
  message: string;
  txHash?: string;
}

export interface VaultState {
  tvlUsd: number;
  liquidReserveUsd: number;
  liquidReservePct: number;
  netApy: number;
  sharpeRatio: number;
  threatLevel: "LOW" | "ELEVATED" | "CRITICAL";
  circuitBreakerActive: boolean;
  strategies: Strategy[];
  logs: TelemetryLog[];
}

export const initialVaultState: VaultState = {
  tvlUsd: 1501000,
  liquidReserveUsd: 226000,
  liquidReservePct: 15.1,
  netApy: 10.45,
  sharpeRatio: 1.28,
  threatLevel: "LOW",
  circuitBreakerActive: false,
  strategies: [
    {
      id: "aave-v3",
      name: "Aave V3 Lending Market",
      protocol: "Aave",
      apy: 8.45,
      allocationUsd: 525000,
      allocationPct: 35.0,
      healthScore: 98.5,
      volatility: 3.8,
      status: "ACTIVE",
      anomalyScore: 0.02,
    },
    {
      id: "morpho-blue",
      name: "Morpho Blue Curated Vault",
      protocol: "Morpho",
      apy: 11.20,
      allocationUsd: 450000,
      allocationPct: 30.0,
      healthScore: 94.0,
      volatility: 6.2,
      status: "ACTIVE",
      anomalyScore: 0.04,
    },
    {
      id: "univ3-lp",
      name: "Uniswap V3 Concentrated LP",
      protocol: "Uniswap",
      apy: 14.80,
      allocationUsd: 300000,
      allocationPct: 20.0,
      healthScore: 89.0,
      volatility: 12.4,
      status: "ACTIVE",
      anomalyScore: 0.08,
    },
  ],
  logs: [
    {
      id: "log-1",
      timestamp: "12:00:14",
      agent: "SYSTEM",
      type: "SUCCESS",
      message: "AegisVault initialized on Base Sepolia. InvariantGuard active.",
    },
    {
      id: "log-2",
      timestamp: "12:01:02",
      agent: "SENTINEL",
      type: "INFO",
      message: "Pool threat telemetry scan clean. Health score avg: 93.8/100.",
    },
    {
      id: "log-3",
      timestamp: "12:01:30",
      agent: "QUANT",
      type: "INFO",
      message: "Computed optimal Sharpe allocation across 3 pools. Projected APY: 10.45%.",
    },
    {
      id: "log-4",
      timestamp: "12:01:31",
      agent: "AUDITOR",
      type: "SUCCESS",
      message: "Invariant verification passed: Max pool 35% <= 40%, Reserve 15% >= 10%. Intent signed.",
      txHash: "0x8fa1...c4b2",
    },
  ],
};
