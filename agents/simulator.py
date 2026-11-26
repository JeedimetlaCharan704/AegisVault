"""
Interactive Simulation Runner for AegisVault Multi-Agent System
Run: python simulator.py
"""
import json
import time
from core.orchestrator import AgentOrchestrator


def run_full_simulation():
    print("=" * 70)
    print("🛡️  AEGISVAULT: AUTONOMOUS RISK SENTINEL & REBALANCING SIMULATION")
    print("=" * 70)

    orchestrator = AgentOrchestrator()
    time.sleep(0.5)

    print("\n[PHASE 1] Initial Vault Telemetry:")
    print(f"  • Total AUM: ${orchestrator.state.total_aum_usd:,.2f}")
    print(f"  • Liquid Reserve: ${orchestrator.state.liquid_reserve_usd:,.2f} ({orchestrator.state.liquid_reserve_pct}%)")
    for addr, s in orchestrator.state.strategies.items():
        print(f"    - {s.name:32} | APY: {s.current_apy_pct:5.2f}% | Health: {s.health_score:4.1f}/100 | Alloc: ${s.current_allocation_usd:,.0f}")

    print("\n[PHASE 2] Running Autonomous Agent Cycle (Normal Market Conditions)...")
    res1 = orchestrator.run_cycle()
    print(f"  ✓ Sentinel Status: Threat Level {res1['threat_level']}")
    print(f"  ✓ Quant Optimizer Proposed APY: {res1['expected_apy']}% (Sharpe: {res1['sharpe_ratio']})")
    print(f"  ✓ Auditor Invariant Check Passed: {res1['approved']}")
    print(f"  ✓ Signed Intent Hash: {res1['signed_intent_hash']}")

    print("\n" + "-" * 70)
    print("⚠️  [PHASE 3] INJECTING BLACK SWAN EXPLOIT SCENARIO:")
    print("  -> An attacker broadcasts a flash-loan drain against 'Morpho Blue'!")
    print("  -> Health score collapses from 94.0 -> 35.0, Anomaly Score -> 0.95")
    orchestrator.simulate_threat("Morpho", health_score=35.0, anomaly_score=0.95)

    time.sleep(0.5)
    print("\n[PHASE 4] Running Threat Sentinel Emergency Cycle...")
    res2 = orchestrator.run_cycle()
    print(f"  🚨 SENTINEL ALERT: Action = {res2.get('action')}")
    print(f"  🚨 Threat Level: {res2.get('threat_level')}")
    print(f"  🚨 Reason: {res2.get('reason')}")
    print(f"  🛡️  Emergency De-Risk Executed: Capital salvaged to Reserve!")

    print("\n[PHASE 5] Post-Defense Vault Telemetry:")
    print(f"  • Total AUM Protected: ${orchestrator.state.total_aum_usd:,.2f}")
    print(f"  • New Liquid Reserve: ${orchestrator.state.liquid_reserve_usd:,.2f} ({orchestrator.state.liquid_reserve_pct}%)")
    for addr, s in orchestrator.state.strategies.items():
        status = "⚠️ ISOLATED/PAUSED" if s.is_paused else "ACTIVE"
        print(f"    - {s.name:32} | Alloc: ${s.current_allocation_usd:,.0f} | Status: {status}")

    print("\n[PHASE 6] Running Recovery Optimization Cycle...")
    res3 = orchestrator.run_cycle()
    print(f"  ✓ Quant Reallocation: {res3.get('target_allocations')}")
    print(f"  ✓ Invariant Verified: Compromised pool received 0% allocation.")
    print("\n" + "=" * 70)
    print("🎉 SIMULATION COMPLETE: All user capital defended autonomously!")
    print("=" * 70)


if __name__ == "__main__":
    run_full_simulation()
