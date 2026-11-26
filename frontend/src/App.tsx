import React, { useState, useEffect } from "react";
import { Navbar } from "./components/minimal/Navbar";
import { VaultSummary } from "./components/minimal/VaultSummary";
import { DepositPanel } from "./components/minimal/DepositPanel";
import { SimpleChart } from "./components/minimal/SimpleChart";
import { AllocationList } from "./components/minimal/AllocationList";
import { GuardrailsSection } from "./components/minimal/GuardrailsSection";
import { ActivityFeed } from "./components/minimal/ActivityFeed";
import { DefenseHUD } from "./components/minimal/DefenseHUD";
import { RegimeOptimizer } from "./components/minimal/RegimeOptimizer";
import { Meteors } from "./components/magic/Meteors";
import { initialVaultState, VaultState, Strategy } from "./lib/simulation-engine";
import {
  fetchLiveVaultState,
  triggerRebalanceBackend,
  triggerAttackBackend,
  triggerDepositBackend,
  triggerResetBackend,
} from "./lib/agent-api";
import { connectBrowserWallet } from "./lib/web3-provider";

export function App() {
  const [vault, setVault] = useState<VaultState>(initialVaultState);
  const [userBalance, setUserBalance] = useState<number>(12450);
  const [activeTab, setActiveTab] = useState<string>("vault");
  const [isDefenseHudOpen, setIsDefenseHudOpen] = useState<boolean>(false);
  const [connectedWallet, setConnectedWallet] = useState<string | null>(null);
  const [isRealWalletConnected, setIsRealWalletConnected] = useState<boolean>(false);

  // Sync with Python Agent Backend on mount
  useEffect(() => {
    async function syncBackendState() {
      const backendState = await fetchLiveVaultState();
      if (backendState) {
        setVault((prev) => ({
          ...prev,
          tvlUsd: backendState.tvlUsd,
          liquidReserveUsd: backendState.liquidReserveUsd,
          liquidReservePct: backendState.liquidReservePct,
          netApy: backendState.netApy,
          sharpeRatio: backendState.sharpeRatio,
          threatLevel: backendState.threatLevel,
          circuitBreakerActive: backendState.circuitBreakerActive,
          strategies: backendState.strategies as Strategy[],
          logs: backendState.logs && backendState.logs.length > 0 ? backendState.logs : prev.logs,
        }));
      }
    }
    syncBackendState();
  }, []);

  const handleConnectWallet = async () => {
    const res = await connectBrowserWallet();
    if (res && res.address) {
      setConnectedWallet(res.address);
      setIsRealWalletConnected(true);
      const newLog = {
        id: `log-${Date.now()}`,
        timestamp: new Date().toLocaleTimeString(),
        agent: "SYSTEM" as const,
        type: "SUCCESS" as const,
        message: `Web3 wallet connected: ${res.address.slice(0, 6)}...${res.address.slice(-4)} on Base Sepolia.`,
      };
      setVault((prev) => ({ ...prev, logs: [...prev.logs, newLog] }));
    }
  };

  const isAttackActive = vault.threatLevel === "CRITICAL";

  const handleDepositSuccess = async (amount: number) => {
    setUserBalance((prev) => Math.max(0, prev - amount));
    const newTvl = vault.tvlUsd + amount;
    const newReserve = vault.liquidReserveUsd + amount;
    const newReservePct = (newReserve / newTvl) * 100;

    const newLog = {
      id: `log-${Date.now()}`,
      timestamp: new Date().toLocaleTimeString(),
      agent: "SYSTEM" as const,
      type: "SUCCESS" as const,
      message: `User deposited $${amount.toLocaleString()} USDC -> Minted ${(amount / 1.0425).toFixed(2)} agUSDC shares.`,
      txHash: "0x4b7e...92f1",
    };

    setVault({
      ...vault,
      tvlUsd: newTvl,
      liquidReserveUsd: newReserve,
      liquidReservePct: newReservePct,
      logs: [...vault.logs, newLog],
    });

    // Notify backend
    await triggerDepositBackend(amount, connectedWallet || "0x71C95911E9a5D330f4D62145069B562089292e");
  };

  const handleApplyRebalance = async (
    regimeLabel: string,
    newApy: number,
    newSharpe: number,
    newReservePct: number,
    newStrategies: Strategy[]
  ) => {
    const newReserveUsd = vault.tvlUsd * (newReservePct / 100);
    const newLog = {
      id: `log-${Date.now()}`,
      timestamp: new Date().toLocaleTimeString(),
      agent: "QUANT" as const,
      type: "SUCCESS" as const,
      message: `Rebalanced portfolio to ${regimeLabel}. Sharpe: ${newSharpe.toFixed(2)}, Projected APY: ${newApy.toFixed(2)}%. All invariant constraints satisfied.`,
      txHash: "0x6f2b...9a41",
    };

    setVault({
      ...vault,
      netApy: newApy,
      sharpeRatio: newSharpe,
      liquidReservePct: newReservePct,
      liquidReserveUsd: newReserveUsd,
      strategies: newStrategies,
      logs: [...vault.logs, newLog],
    });

    // Trigger backend agent solver & EIP-712 signing
    const regimeKey = regimeLabel.includes("Surge")
      ? "AGGRESSIVE"
      : regimeLabel.includes("Fortress")
      ? "DEFENSIVE"
      : "BALANCED";
    await triggerRebalanceBackend(regimeKey);
  };

  const handleTriggerAttack = async () => {
    const updatedStrategies = vault.strategies.map((strat) => {
      if (strat.id === "morpho-blue" || strat.id.includes("morpho")) {
        return {
          ...strat,
          healthScore: 32.0,
          anomalyScore: 0.96,
          allocationUsd: 0,
          allocationPct: 0,
          status: "PAUSED" as const,
        };
      }
      return strat;
    });

    const newLogs = [
      ...vault.logs,
      {
        id: `log-${Date.now()}-1`,
        timestamp: new Date().toLocaleTimeString(),
        agent: "SENTINEL" as const,
        type: "CRITICAL" as const,
        message: "🚨 Anomaly detected: Morpho Blue health dropped to 32.0/100. Intercepted flash-loan pattern.",
      },
      {
        id: `log-${Date.now()}-2`,
        timestamp: new Date().toLocaleTimeString(),
        agent: "SENTINEL" as const,
        type: "SUCCESS" as const,
        message: "🛡️ Recalled $450,000 from Morpho Blue into safe liquid reserve. Target delisted.",
        txHash: "0x3e9b...a71c",
      },
      {
        id: `log-${Date.now()}-3`,
        timestamp: new Date().toLocaleTimeString(),
        agent: "AUDITOR" as const,
        type: "SUCCESS" as const,
        message: "Invariant verify: Reserve elevated to 45.0% (>= 10.0% floor). Zero capital lost.",
        txHash: "0x1d4f...99e2",
      },
    ];

    setVault({
      ...vault,
      liquidReserveUsd: 675000,
      liquidReservePct: 45.0,
      threatLevel: "CRITICAL",
      netApy: 7.20,
      sharpeRatio: 1.65,
      strategies: updatedStrategies,
      logs: newLogs,
    });

    setIsDefenseHudOpen(true);

    // Call Python backend
    await triggerAttackBackend();
  };

  const handleResetVault = async () => {
    setVault(initialVaultState);
    await triggerResetBackend();
  };

  return (
    <div className="min-h-screen bg-[#07080b] text-zinc-100 flex flex-col justify-between selection:bg-zinc-800 selection:text-white w-full relative overflow-x-hidden">
      {/* Magic UI Subtle Ambient Meteors in Background */}
      <Meteors number={12} />

      <div className="w-full relative z-10">
        {/* Widescreen Minimal Navbar */}
        <Navbar
          userBalance={userBalance}
          activeTab={activeTab}
          setActiveTab={setActiveTab}
          connectedAddress={connectedWallet || "0x71C95911E9a5D330f4D62145069B562089292e"}
          isRealWalletConnected={isRealWalletConnected}
          onConnectWallet={handleConnectWallet}
        />

        {/* Widescreen Laptop Main Container with Generous Spacing */}
        <main className="max-w-[1440px] w-full mx-auto px-6 sm:px-8 lg:px-10 pt-4 space-y-8 pb-12">
          {/* Header Summary with 4 Spotlight KPI Cards & NumberTicker */}
          <div id="vault">
            <VaultSummary
              tvl={vault.tvlUsd}
              netApy={vault.netApy}
              sharpeRatio={vault.sharpeRatio}
              liquidReserve={vault.liquidReserveUsd}
              liquidReservePct={vault.liquidReservePct}
              isAttackActive={isAttackActive}
            />
          </div>

          {/* Widescreen 2-Column Split: 8 cols (67%) Left, 4 cols (33%) Right */}
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
            {/* Left Main Dashboard (8 columns) */}
            <div className="lg:col-span-8 space-y-8">
              {/* Expansive SVG Performance Trajectory Curve with Spotlight */}
              <SimpleChart />

              {/* Quantitative Market Risk Regime Optimizer ("What-If" Rebalancing Engine) */}
              <div id="regimes">
                <RegimeOptimizer
                  tvl={vault.tvlUsd}
                  currentStrategies={vault.strategies}
                  onApplyRebalance={handleApplyRebalance}
                />
              </div>

              {/* Full Strategy Table with Progress Bar */}
              <div id="strategies">
                <AllocationList
                  strategies={vault.strategies}
                  liquidReserveUsd={vault.liquidReserveUsd}
                  liquidReservePct={vault.liquidReservePct}
                />
              </div>

              {/* On-Chain Security & Invariants with Spotlight & Shimmer trigger */}
              <div id="security">
                <GuardrailsSection
                  threatLevel={vault.threatLevel}
                  onTriggerAttack={handleTriggerAttack}
                  onResetVault={handleResetVault}
                />
              </div>
            </div>

            {/* Right Action & Activity Sidebar (4 columns) */}
            <div className="lg:col-span-4 space-y-8">
              {/* Deposit & Withdraw Box with Spotlight & Shimmer Button */}
              <DepositPanel
                userBalance={userBalance}
                netApy={vault.netApy}
                onDepositSuccess={handleDepositSuccess}
              />

              {/* Real-Time Activity & Audit Feed */}
              <div id="activity">
                <ActivityFeed logs={vault.logs} />
              </div>
            </div>
          </div>
        </main>
      </div>

      {/* Cyber Defense Shield Shockwave HUD */}
      <DefenseHUD
        isOpen={isDefenseHudOpen}
        onClose={() => setIsDefenseHudOpen(false)}
      />

      {/* Widescreen Minimal Footer */}
      <footer className="border-t border-white/[0.08] py-5 px-6 lg:px-10 text-xs text-zinc-500 font-mono w-full relative z-10">
        <div className="max-w-[1440px] mx-auto flex flex-col sm:flex-row items-center justify-between gap-3">
          <span>Aegis Protocol · Base Sepolia (84532) · Vault: 0x8920...43e7</span>
          <div className="flex items-center gap-6 text-zinc-400 text-xs">
            <span>ERC-4626 Tokenized Vault</span>
            <span>InvariantGuard Active</span>
            <span>Multi-Agent Consensus (3/3 Online)</span>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
