#!/usr/bin/env python3
"""
AegisVault Institutional Developer CLI
Command-line interface to inspect, rebalance, simulate defense, and audit AegisVault.

Usage:
  python cli.py status
  python cli.py rebalance --regime [BALANCED|AGGRESSIVE|DEFENSIVE]
  python cli.py attack
  python cli.py keeper
  python cli.py keys
  python cli.py reset
"""

import os
import sys
import argparse
import json
import urllib.request
import urllib.error
from dotenv import load_dotenv

load_dotenv()
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
load_dotenv(os.path.join(os.path.dirname(__file__), "agents", ".env"))

API_URL = os.getenv("AGENT_SERVER_URL", "http://localhost:8000")


def print_banner():
    banner = """
    ╔═══════════════════════════════════════════════════════════════════╗
    ║                     🛡️  AEGISVAULT (SENTINEL-4626)                ║
    ║        Autonomous Multi-Agent Co-Processor & Invariant Guard     ║
    ╚═══════════════════════════════════════════════════════════════════╝
    """
    print(banner)


def cmd_keys():
    print_banner()
    deployer = os.getenv("DEPLOYER_ADDRESS", "0x1a099FF069aDF6c45efBFc72FB0967A01FB3a026")
    agent_signer = os.getenv("AGENT_SIGNER_ADDRESS", "0x2A6261d5e6ce20456aad4Bdf59a30C9CD243f260")
    rpc = os.getenv("RPC_URL", "https://sepolia.base.org")
    chain_id = os.getenv("CHAIN_ID", "84532")

    print("🔑 CONFIGURED CRYPTOGRAPHIC IDENTITIES:")
    print(f"  • Network: Base Sepolia (Chain ID: {chain_id})")
    print(f"  • RPC URL: {rpc}")
    print(f"  • Deployer Account: {deployer}")
    print(f"  • Agent Signer:     {agent_signer}")
    print(f"  • Contract Vault:   0x89209581A7bF892c23F1E7b4C198F908381243e7")
    print(f"  • InvariantGuard:   0x7B114389e8B7E5830AcF65d098e9a2632bEb94a2")
    print("=" * 70)


def cmd_status():
    print_banner()
    try:
        req = urllib.request.Request(f"{API_URL}/api/vault/state")
        with urllib.request.urlopen(req, timeout=4) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"⚠️  Could not reach Agent Server at {API_URL}: {e}")
        print("Run 'python agents/server.py' to start the co-processor.")
        return

    print("📊 LIVE ON-CHAIN VAULT TELEMETRY:")
    print(f"  • Total Assets (TVL):   ${data.get('tvlUsd', 0):,.2f}")
    print(f"  • Liquid Cash Reserve:  ${data.get('liquidReserveUsd', 0):,.2f} ({data.get('liquidReservePct', 0):.1f}%) [Floor: >= 10.0%]")
    print(f"  • Net Strategy APY:     {data.get('netApy', 0):.2f}%")
    print(f"  • Sharpe Ratio:         {data.get('sharpeRatio', 0):.2f} (Rf: 4.5% Benchmark)")
    print(f"  • Threat Level:         {data.get('threatLevel', 'LOW')}")
    print(f"  • Circuit Breaker:      {'🚨 ACTIVE' if data.get('circuitBreakerActive') else '✅ NORMAL'}")
    print("-" * 70)

    print("🏛️  ALLOCATION & YIELD MARKETS:")
    print(f"  {'Protocol / Market':<32} {'Net APY':<10} {'Allocation':<16} {'Weight':<10} {'Health'}")
    print(f"  {'-'*30} {'-'*8} {'-'*14} {'-'*8} {'-'*8}")

    for s in data.get("strategies", []):
        alloc_str = f"${s['allocationUsd']:,.0f}"
        status_flag = " [PAUSED]" if s.get("status") == "PAUSED" else ""
        print(f"  {s['name'][:30]:<32} {s['apy']:>5.2f}%   {alloc_str:>14}  {s['allocationPct']:>5.1f}%   {s['healthScore']:>4.1f}/100{status_flag}")

    print("=" * 70)


def cmd_rebalance(regime: str):
    print_banner()
    print(f"⚡ DISPATCHING QUANT AGENT REBALANCE -> Regime: {regime.upper()}...")
    try:
        body = json.dumps({"regime": regime.upper()}).encode("utf-8")
        req = urllib.request.Request(
            f"{API_URL}/api/agents/rebalance",
            data=body,
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            print(f"✅ REBALANCE EXECUTED:")
            print(f"  • Regime:        {data.get('regime')}")
            print(f"  • New Net APY:   {data.get('netApy')}%")
            print(f"  • Sharpe Ratio:  {data.get('sharpeRatio')}")
            print(f"  • EIP-712 Sig:   {data.get('signature')}")
    except Exception as e:
        print(f"❌ Rebalance failed: {e}")


def cmd_attack():
    print_banner()
    print("🚨 INJECTING FLASH-LOAN ATTACK ANOMALY AGAINST MORPHO BLUE...")
    try:
        req = urllib.request.Request(
            f"{API_URL}/api/agents/simulate-attack",
            data=b"{}",
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            print("🛡️  SENTINEL DEFENSE TRIGGERED:")
            print(f"  • Threat Level:     {data.get('threatLevel')}")
            print(f"  • Action:           {data.get('action')}")
            print(f"  • Salvaged Reserve: {data.get('salvagedReservePct')}% (Elevated safely)")
            print(f"  • Defense Tx Sig:   {data.get('signature')}")
    except Exception as e:
        print(f"❌ Exploit simulation failed: {e}")


def cmd_reset():
    print_banner()
    try:
        req = urllib.request.Request(f"{API_URL}/api/vault/reset", data=b"{}")
        with urllib.request.urlopen(req, timeout=4) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            print("✅ Vault state reset to baseline parameters.")
    except Exception as e:
        print(f"❌ Reset failed: {e}")


def main():
    parser = argparse.ArgumentParser(description="AegisVault Institutional Developer CLI")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("status", help="Display live vault telemetry and strategies")
    subparsers.add_parser("keys", help="Display configured keys and RPC endpoints")
    subparsers.add_parser("attack", help="Simulate flash-loan exploit and Sentinel reaction")
    subparsers.add_parser("reset", help="Reset vault state to baseline")

    rebalance_parser = subparsers.add_parser("rebalance", help="Execute Quant Agent MPT rebalance")
    rebalance_parser.add_argument("--regime", choices=["BALANCED", "AGGRESSIVE", "DEFENSIVE"], default="BALANCED")

    args = parser.parse_args()

    if args.command == "status":
        cmd_status()
    elif args.command == "keys":
        cmd_keys()
    elif args.command == "rebalance":
        cmd_rebalance(args.regime)
    elif args.command == "attack":
        cmd_attack()
    elif args.command == "reset":
        cmd_reset()
    else:
        cmd_status()


if __name__ == "__main__":
    main()
