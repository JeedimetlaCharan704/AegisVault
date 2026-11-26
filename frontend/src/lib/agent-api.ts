/**
 * Agent API Client Bridge for AegisVault
 * Connects the React 19 Frontend directly to the Python Multi-Agent Co-Processor (FastAPI).
 * Automatically falls back to client-side state if the backend server is temporarily paused.
 */

const BACKEND_BASE_URL = "http://localhost:8000";

export interface BackendVaultState {
  tvlUsd: number;
  liquidReserveUsd: number;
  liquidReservePct: number;
  netApy: number;
  sharpeRatio: number;
  threatLevel: "LOW" | "ELEVATED" | "CRITICAL";
  circuitBreakerActive: boolean;
  strategies: Array<{
    id: string;
    name: string;
    protocol: string;
    apy: number;
    allocationUsd: number;
    allocationPct: number;
    healthScore: number;
    volatility: number;
    status: "ACTIVE" | "PAUSED" | "COMPROMISED";
    anomalyScore: number;
  }>;
  agentSigner?: string;
  network?: string;
  logs?: any[];
}

export async function checkBackendHealth(): Promise<boolean> {
  try {
    const res = await fetch(`${BACKEND_BASE_URL}/`, { method: "GET" });
    return res.ok;
  } catch {
    return false;
  }
}

export async function fetchLiveVaultState(): Promise<BackendVaultState | null> {
  try {
    const res = await fetch(`${BACKEND_BASE_URL}/api/vault/state`, {
      method: "GET",
      headers: { "Content-Type": "application/json" },
    });
    if (!res.ok) return null;
    return await res.json();
  } catch (err) {
    console.warn("Backend not reachable, operating in autonomous local fallback mode:", err);
    return null;
  }
}

export async function triggerRebalanceBackend(regime: string): Promise<any | null> {
  try {
    const res = await fetch(`${BACKEND_BASE_URL}/api/agents/rebalance`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ regime }),
    });
    if (!res.ok) return null;
    return await res.json();
  } catch (err) {
    console.warn("Rebalance backend call failed, fallback to local:", err);
    return null;
  }
}

export async function triggerAttackBackend(): Promise<any | null> {
  try {
    const res = await fetch(`${BACKEND_BASE_URL}/api/agents/simulate-attack`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ targetProtocol: "Morpho", healthScore: 32.0, anomalyScore: 0.96 }),
    });
    if (!res.ok) return null;
    return await res.json();
  } catch (err) {
    console.warn("Attack simulation backend call failed, fallback to local:", err);
    return null;
  }
}

export async function triggerDepositBackend(amountUsd: number, userAddress: string): Promise<any | null> {
  try {
    const res = await fetch(`${BACKEND_BASE_URL}/api/vault/deposit`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ amountUsd, userAddress }),
    });
    if (!res.ok) return null;
    return await res.json();
  } catch (err) {
    console.warn("Deposit backend call failed, fallback to local:", err);
    return null;
  }
}

export async function triggerResetBackend(): Promise<any | null> {
  try {
    const res = await fetch(`${BACKEND_BASE_URL}/api/vault/reset`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
    });
    if (!res.ok) return null;
    return await res.json();
  } catch (err) {
    console.warn("Reset backend call failed, fallback to local:", err);
    return null;
  }
}
