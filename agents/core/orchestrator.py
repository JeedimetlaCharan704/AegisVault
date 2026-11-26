"""
Master Multi-Agent Orchestrator for AegisVault
Manages the continuous cycle:
  1. Ingest telemetry from Vault & external DeFi protocols
  2. Threat Sentinel scans for depegs and exploits
  3. Quant Optimizer generates risk-adjusted Sharpe allocation
  4. Auditor Agent verifies mathematical invariants
  5. Relays signed action on-chain
"""
import json
import time
from typing import Dict, Any
from .state import (
    StrategyMetrics,
    AgentSystemState,
)
from .sentinel_agent import SentinelAgent
from .quant_agent import QuantAgent
from .auditor_agent import AuditorAgent


class AgentOrchestrator:
    def __init__(self, gemini_api_key: str = None):
        self.sentinel = SentinelAgent(gemini_api_key)
        self.quant = QuantAgent()
        self.auditor = AuditorAgent()

        # Initial mock state for out-of-the-box execution
        self.state = AgentSystemState(
            vault_address="0x89205A3A3b2A69De6Dbf7f01ED13B2108B2c43e7",
            total_aum_usd=1_500_000.00,
            liquid_reserve_usd=225_000.00,
            liquid_reserve_pct=15.0,
            strategies={
                "0xAaveV3USDC": StrategyMetrics(
                    address="0xAaveV3USDC",
                    name="Aave V3 Lending Market",
                    current_allocation_usd=525_000.00,
                    allocation_pct=35.0,
                    current_apy_pct=8.45,
                    health_score=98.5,
                    volatility_7d=3.8,
                ),
                "0nMorphoBlue": StrategyMetrics(
                    address="0nMorphoBlue",
                    name="Morpho Blue Curated Vault",
                    current_allocation_usd=450_000.00,
                    allocation_pct=30.0,
                    current_apy_pct=11.20,
                    health_score=94.0,
                    volatility_7d=6.2,
                ),
                "0xUniV3USDCETH": StrategyMetrics(
                    address="0xUniV3USDCETH",
                    name="Uniswap V3 Concentrated LP",
                    current_allocation_usd=300_000.00,
                    allocation_pct=20.0,
                    current_apy_pct=14.80,
                    health_score=89.0,
                    volatility_7d=12.4,
                ),
            },
        )

    def run_cycle(self) -> Dict[str, Any]:
        """
        Executes one full iteration of the multi-agent decision loop.
        """
        # Step 1: Threat Sentinel Inspection
        sentinel_report = self.sentinel.inspect_protocols(self.state.strategies)
        self.state.latest_sentinel_report = sentinel_report

        # Step 2: Emergency Response check
        if sentinel_report.emergency_action_required:
            action_log = {
                "timestamp": time.time(),
                "action": "EMERGENCY_DERISK",
                "compromised": sentinel_report.compromised_strategies,
                "threat_level": sentinel_report.threat_level.value,
                "reason": sentinel_report.reasoning,
                "status": "EXECUTED",
            }
            # Salvage funds from compromised strategies back to reserve
            for comp in sentinel_report.compromised_strategies:
                if comp in self.state.strategies:
                    salvaged = self.state.strategies[comp].current_allocation_usd
                    self.state.strategies[comp].current_allocation_usd = 0.0
                    self.state.strategies[comp].allocation_pct = 0.0
                    self.state.strategies[comp].is_paused = True
                    self.state.liquid_reserve_usd += salvaged

            self.state.liquid_reserve_pct = round(
                (self.state.liquid_reserve_usd / self.state.total_aum_usd) * 100, 2
            )
            self.state.execution_history.append(action_log)
            return action_log

        # Step 3: Quant Optimization
        quant_plan = self.quant.generate_optimal_allocation(
            self.state.total_aum_usd,
            self.state.strategies,
            sentinel_report,
        )
        self.state.latest_quant_plan = quant_plan

        # Step 4: Auditor Invariant Verification
        decision = self.auditor.verify_plan(quant_plan, sentinel_report)
        self.state.latest_auditor_decision = decision

        # Step 5: Log execution
        result = {
            "timestamp": time.time(),
            "action": "REBALANCE" if decision.is_approved else "REJECTED_BY_AUDITOR",
            "threat_level": sentinel_report.threat_level.value,
            "target_allocations": quant_plan.target_allocations,
            "expected_apy": quant_plan.expected_portfolio_apy,
            "sharpe_ratio": quant_plan.expected_sharpe_ratio,
            "approved": decision.is_approved,
            "violations": decision.violations,
            "signed_intent_hash": decision.signed_intent_hash,
        }
        self.state.execution_history.append(result)
        return result

    def simulate_threat(self, strategy_key: str, health_score: float, anomaly_score: float = 0.0):
        """
        Injects an artificial exploit or depeg to test Sentinel Agent reaction.
        """
        for addr, s in self.state.strategies.items():
            if strategy_key.lower() in s.name.lower() or strategy_key.lower() in addr.lower():
                s.health_score = health_score
                s.last_tx_anomaly_score = anomaly_score
                break
