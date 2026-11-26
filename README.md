# 🛡️ AegisVault (SentinEL-4626)
### *Autonomous Threat-Sentinel & Dynamic Rebalancing Engine for Tokenized ERC-4626 Vaults with On-Chain Invariant Guardrails*

---

## 🌟 Executive Summary
**AegisVault** bridges the gap between **DeFi Yield Optimization** (Yearn, Sommelier, Morpho) and **Automated Web3 Security** (Hypernative, Forta, Drosera). 

Traditional DeFi vaults either blindly chase yield without real-time threat intelligence or require slow, manual governance interventions during black swan attacks. Conversely, existing security networks can pause contracts, but do not manage liquidity or optimize yields.

**AegisVault unifies both disciplines into an autonomous, self-defending financial primitive:**
* **Threat Sentinel Agent:** Continuously inspects pool reserve ratios, volatility spikes, and mempool signatures to detect depegs, flash loans, and pool drain attacks before finality.
* **Quant Optimization Agent:** Formulates Sharpe-ratio optimal allocations across whitelisted lending markets (Aave, Morpho) and DEX liquidity pools.
* **Auditor / Policy Agent:** Pre-flight checks the mathematical invariant bounds and cryptographically signs valid execution intents.
* **On-Chain InvariantGuard (Solidity):** Enforces hard-coded circuit breakers on-chain ($0.5\%$ slippage cap, $40\%$ single-pool allocation ceiling, $10\%$ liquid reserve floor). **The AI agent physically cannot drain the vault or violate constraints.**

---

## 🏛️ Architecture Overview

```
                          ┌────────────────────────────────────────────────────────┐
                          │               OFF-CHAIN MULTI-AGENT BRAIN              │
                          │                                                        │
┌─────────────────┐       │   ┌───────────────────┐    ┌────────────────────────┐  │
│ Live Data Feeds │       │   │  Sentinel Agent   │    │      Quant Agent       │  │
│ (Pyth, TheGraph,├───────┼──►│  (Exploits,       │    │   (Sharpe Optimizer,   │  │
│  DEX Pools)     │       │   │   Depegs, Anomaly)│    │    Gas vs Yield Model) │  │
└─────────────────┘       │   └─────────┬─────────┘    └───────────┬────────────┘  │
                          │             │                          │               │
                          │             └───────────┬──────────────┘               │
                          │                         ▼                              │
                          │            ┌─────────────────────────┐                 │
                          │            │   Policy / Guard Agent  │                 │
                          │            │ (Validates against caps)│                 │
                          │            └────────────┬────────────┘                 │
                          └─────────────────────────┼──────────────────────────────┘
                                                    │ Signed EIP-712 Intent
                                                    ▼
                          ┌────────────────────────────────────────────────────────┐
                          │               ON-CHAIN SMART CONTRACTS                 │
                          │                                                        │
                          │   ┌────────────────────────────────────────────────┐   │
                          │   │         Aegis ERC-4626 Vault                   │   │
                          │   │   - Holds user deposits (USDC/ETH)             │   │
                          │   │   - Enforces Mathematical Invariants:          │   │
                          │   │       • Max 0.5% slippage cap                  │   │
                          │   │       • Strictly whitelisted routers           │   │
                          │   │       • Max single-pool allocation (40%)       │   │
                          │   │       • Hard Drawdown Circuit Breaker          │   │
                          │   └────────────────────────────────────────────────┘   │
                          │                            │                           │
                          │              Rebalance / De-Risk Actions               │
                          │                            ▼                           │
                          │     [Aave V3]   ──   [Morpho]   ──   [Uniswap V3]      │
                          └────────────────────────────────────────────────────────┘
```

---

## 📂 Project Structure

```
aegis-vault/
├── contracts/                        # Solidity Contracts & Testing
│   ├── src/
│   │   ├── AegisVault.sol           # Core ERC-4626 Vault with Agent Delegation
│   │   ├── InvariantGuard.sol       # Mathematical Invariant & Slippage Guard
│   │   ├── interfaces/
│   │   │   └── IStrategy.sol        # Standardized DeFi strategy interface
│   │   └── mocks/
│   │       └── MockStrategy.sol     # Simulates Aave/Morpho with anomaly injection
│   ├── test/
│   │   └── run-tests.js             # Automated compilation & invariant testing
│   └── scripts/
│       └── deploy.js                # Deployment pipeline
│
├── agents/                           # Python Multi-Agent Intelligence
│   ├── core/
│   │   ├── state.py                 # Telemetry & Agent System State models
│   │   ├── sentinel_agent.py        # Threat, exploit & depeg detection
│   │   ├── quant_agent.py           # Sharpe-ratio yield allocation optimizer
│   │   ├── auditor_agent.py         # On-chain invariant pre-flight verification
│   │   └── orchestrator.py          # Master loop coordinating all agents
│   └── simulator.py                 # Interactive terminal scenario generator
│
└── frontend/                         # React/Next.js Financial Command Center
    ├── src/
    │   ├── components/              # BentoGrid, ThreatRadar, InvariantMatrix
    │   └── App.tsx                  # Interactive "Black Swan" Attack Simulator
    └── tailwind.config.js           # Dark mode cyber/fintech theme
```

---

## ⚡ Quick Start Guide

### 1. Smart Contracts Verification
```bash
cd contracts
node test/run-tests.js
```
*Compiles all Solidity code and mathematically proves all 4 invariant rules hold.*

### 2. Multi-Agent System & Attack Simulation
```bash
cd agents
python simulator.py
```
*Executes the autonomous loop: Normal optimization $\rightarrow$ Injects a flash-loan drain $\rightarrow$ Sentinel triggers Emergency De-Risk $\rightarrow$ $450k capital salvaged to safety.*

### 3. Frontend Command Center
```bash
cd frontend
npm run dev
```
*Launches the high-end dark mode dashboard at `http://localhost:5173`.*

---

## 🔒 Security Invariants (Mathematical Proofs)

1. **Max Pool Allocation**:
   $$\sum \text{Assets}_{\text{strategy}_i} \le 0.40 \times \text{TotalAUM}$$
2. **Minimum Liquid Reserve**:
   $$\text{Reserve}_{\text{liquid}} \ge 0.10 \times \text{TotalAUM}$$
3. **Max Slippage**:
   $$\text{Slippage}_{\text{rebalance}} \le 0.5\% \quad (50 \text{ BPS})$$
4. **Drawdown Circuit Breaker**:
   $$\Delta \text{AUM}_{\text{1-hour}} \ge 5\% \implies \text{Vault Paused}$$
