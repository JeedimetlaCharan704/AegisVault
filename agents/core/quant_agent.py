"""
Quant Optimization Agent for AegisVault
Computes risk-adjusted yield allocations using modern portfolio theory (Sharpe optimization)
subject to on-chain invariant bounds.
"""
import time
from typing import Dict, List
from .state import StrategyMetrics, QuantAllocationPlan, SentinelReport


class QuantAgent:
    def __init__(self, risk_free_rate: float = 0.045):
        self.name = "Aegis-Quant-01"
        self.risk_free_rate = risk_free_rate  # 4.5% baseline benchmark (US Treasury / Dai sDAI)
        self.max_allocation_cap = 0.40       # Max 40% per pool
        self.min_reserve_target = 0.15       # Target 15% liquid reserve

    def generate_optimal_allocation(
        self,
        total_aum: float,
        strategies: Dict[str, StrategyMetrics],
        sentinel_report: SentinelReport,
    ) -> QuantAllocationPlan:
        """
        Formulates the mathematically optimal allocation plan.
        """
        valid_strategies = {}
        for addr, s in strategies.items():
            if addr not in sentinel_report.compromised_strategies and not s.is_paused:
                valid_strategies[addr] = s

        allocations: Dict[str, float] = {}

        if not valid_strategies:
            # 100% into safe reserve if all strategies are compromised
            allocations["RESERVE"] = 1.0
            return QuantAllocationPlan(
                timestamp=time.time(),
                target_allocations=allocations,
                expected_portfolio_apy=0.0,
                expected_sharpe_ratio=0.0,
                gas_cost_estimate_usd=0.0,
                net_alpha_gain_usd=0.0,
                explanation="DEFENSIVE LOCKDOWN: All external strategies compromised. 100% allocation to liquid reserve.",
            )

        # Calculate risk-adjusted scores (APY / Volatility)
        scores = {}
        for addr, s in valid_strategies.items():
            vol = max(s.volatility_7d, 2.0)  # floor at 2% to avoid div zero
            excess_return = max(s.current_apy_pct - (self.risk_free_rate * 100), 0.5)
            score = excess_return / vol
            scores[addr] = score

        total_score = sum(scores.values()) or 1.0
        investable_capital_pct = 1.0 - self.min_reserve_target

        # Distribute based on Sharpe weighting with 40% hard cap
        remaining_pct = investable_capital_pct
        for addr, score in sorted(scores.items(), key=lambda x: x[1], reverse=True):
            raw_weight = (score / total_score) * investable_capital_pct
            weight = min(raw_weight, self.max_allocation_cap)
            allocations[addr] = round(weight, 4)
            remaining_pct -= weight

        # Add remaining to reserve
        allocations["RESERVE"] = round(self.min_reserve_target + max(remaining_pct, 0.0), 4)

        # Expected portfolio metrics
        expected_apy = sum(
            allocations.get(addr, 0.0) * strategies[addr].current_apy_pct
            for addr in valid_strategies
        )
        avg_vol = sum(
            allocations.get(addr, 0.0) * strategies[addr].volatility_7d
            for addr in valid_strategies
        ) or 5.0
        sharpe = round((expected_apy - (self.risk_free_rate * 100)) / avg_vol, 2)

        est_gas_usd = 4.50  # Average L2 Base transaction batch cost
        net_alpha = round((total_aum * (expected_apy / 100) / 365) - est_gas_usd, 2)

        explanation = (
            f"Optimized {len(valid_strategies)} strategies. Max Sharpe allocation: "
            f"Reserve: {allocations['RESERVE']*100:.1f}%, Top Strategy: {max(allocations.values())*100:.1f}%. "
            f"Projected Annual APY: {expected_apy:.2f}% (Sharpe: {sharpe})."
        )

        return QuantAllocationPlan(
            timestamp=time.time(),
            target_allocations=allocations,
            expected_portfolio_apy=round(expected_apy, 2),
            expected_sharpe_ratio=sharpe,
            gas_cost_estimate_usd=est_gas_usd,
            net_alpha_gain_usd=net_alpha,
            explanation=explanation,
        )
