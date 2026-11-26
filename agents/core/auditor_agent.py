"""
Auditor & Policy Agent for AegisVault
Pre-flight verification engine: Validates that all proposed rebalancing actions
strictly satisfy on-chain InvariantGuard rules before signing transaction intents.
"""
import hashlib
import json
import time
from typing import Dict, List
from .state import (
    QuantAllocationPlan,
    SentinelReport,
    AuditorDecision,
)


class AuditorAgent:
    def __init__(
        self,
        max_pool_allocation_pct: float = 0.40,
        min_reserve_pct: float = 0.10,
    ):
        self.name = "Aegis-Auditor-01"
        self.max_pool_cap = max_pool_allocation_pct
        self.min_reserve = min_reserve_pct

    def verify_plan(
        self,
        plan: QuantAllocationPlan,
        sentinel_report: SentinelReport,
    ) -> AuditorDecision:
        """
        Executes strict invariant audits on the proposed quant plan.
        """
        violations: List[str] = []
        checks = {}

        # Invariant Check 1: Max single pool allocation
        pool_caps_satisfied = True
        for target, weight in plan.target_allocations.items():
            if target != "RESERVE" and weight > self.max_pool_cap + 0.0001:
                violations.append(
                    f"Invariant Violated: Strategy {target} allocation {weight*100:.1f}% exceeds max allowed {self.max_pool_cap*100:.1f}%."
                )
                pool_caps_satisfied = False
        checks["MAX_ALLOCATION_CAP_40%"] = pool_caps_satisfied

        # Invariant Check 2: Minimum liquid reserve invariant
        reserve_weight = plan.target_allocations.get("RESERVE", 0.0)
        reserve_satisfied = reserve_weight >= self.min_reserve - 0.0001
        if not reserve_satisfied:
            violations.append(
                f"Invariant Violated: Liquid reserve {reserve_weight*100:.1f}% is below minimum required {self.min_reserve*100:.1f}%."
            )
        checks["MIN_LIQUID_RESERVE_10%"] = reserve_satisfied

        # Invariant Check 3: Zero allocation to compromised strategies
        compromised_clean = True
        for comp_addr in sentinel_report.compromised_strategies:
            if plan.target_allocations.get(comp_addr, 0.0) > 0.0:
                violations.append(
                    f"Invariant Violated: Plan allocated funds to compromised strategy {comp_addr}!"
                )
                compromised_clean = False
        checks["ZERO_COMPROMISED_ALLOCATION"] = compromised_clean

        is_approved = len(violations) == 0

        # Generate cryptographic intent digest
        signed_hash = None
        if is_approved:
            payload = {
                "timestamp": plan.timestamp,
                "allocations": plan.target_allocations,
                "expected_apy": plan.expected_portfolio_apy,
            }
            raw = json.dumps(payload, sort_keys=True).encode("utf-8")
            signed_hash = "0x" + hashlib.sha256(raw).hexdigest()

        return AuditorDecision(
            timestamp=time.time(),
            is_approved=is_approved,
            violations=violations,
            invariants_checked=checks,
            signed_intent_hash=signed_hash,
        )
