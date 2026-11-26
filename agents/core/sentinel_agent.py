"""
Threat Sentinel Agent for AegisVault
Monitors real-time protocol health, pool reserves, oracle deviations, and exploit patterns.
"""
import time
from typing import Dict, List
from .state import (
    StrategyMetrics,
    SentinelReport,
    ThreatLevel,
    AnomalyType,
)


class SentinelAgent:
    def __init__(self, gemini_api_key: str = None):
        self.name = "Aegis-Sentinel-01"
        self.gemini_api_key = gemini_api_key

    def inspect_protocols(self, strategies: Dict[str, StrategyMetrics]) -> SentinelReport:
        """
        Analyzes strategy telemetry to detect hacks, flash loan drains, or depeg threats.
        """
        compromised = []
        highest_threat = ThreatLevel.LOW
        detected_anomaly = AnomalyType.NORMAL
        reasoning_points = []

        for addr, strat in strategies.items():
            # Check 1: Severe Health Score Deterioration
            if strat.health_score < 60:
                compromised.append(addr)
                highest_threat = ThreatLevel.CRITICAL
                detected_anomaly = AnomalyType.FLASH_LOAN_DRAIN
                reasoning_points.append(
                    f"CRITICAL: {strat.name} health score crashed to {strat.health_score}/100. Potential flash loan or pool drain in progress."
                )
            elif strat.health_score < 75:
                if highest_threat not in [ThreatLevel.CRITICAL]:
                    highest_threat = ThreatLevel.HIGH
                detected_anomaly = AnomalyType.DEPEG
                reasoning_points.append(
                    f"WARNING: {strat.name} health score degraded to {strat.health_score}/100. Underlying liquidity depth dropping."
                )

            # Check 2: Volatility Spikes
            if strat.volatility_7d > 45.0:
                if highest_threat == ThreatLevel.LOW:
                    highest_threat = ThreatLevel.MEDIUM
                reasoning_points.append(
                    f"ELEVATED RISK: {strat.name} 7-day annualized volatility spiked to {strat.volatility_7d}%."
                )

            # Check 3: Mempool Anomaly Score
            if strat.last_tx_anomaly_score > 0.8:
                compromised.append(addr)
                highest_threat = ThreatLevel.CRITICAL
                detected_anomaly = AnomalyType.FLASH_LOAN_DRAIN
                reasoning_points.append(
                    f"EXPLOIT PATTERN DETECTED: {strat.name} transaction volume shows anomalous repetitive borrow/swap signature."
                )

        emergency_needed = highest_threat in [ThreatLevel.CRITICAL, ThreatLevel.HIGH] and len(compromised) > 0

        summary = (
            " | ".join(reasoning_points)
            if reasoning_points
            else "All active strategies operating within normal volatility and liquidity bounds. No anomalies detected."
        )

        return SentinelReport(
            timestamp=time.time(),
            threat_level=highest_threat,
            anomaly_detected=detected_anomaly,
            compromised_strategies=compromised,
            confidence_score=0.96 if emergency_needed else 0.99,
            emergency_action_required=emergency_needed,
            reasoning=summary,
        )
