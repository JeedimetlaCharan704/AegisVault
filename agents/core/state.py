"""
State and Data Models for AegisVault Multi-Agent Engine
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional
import time


class ThreatLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class AnomalyType(str, Enum):
    NORMAL = "NORMAL"
    DEPEG = "DEPEG"
    FLASH_LOAN_DRAIN = "FLASH_LOAN_DRAIN"
    ORACLE_DIVERGENCE = "ORACLE_DIVERGENCE"
    VOLATILITY_SPIKE = "VOLATILITY_SPIKE"


@dataclass
class StrategyMetrics:
    address: str
    name: str
    current_allocation_usd: float
    allocation_pct: float
    current_apy_pct: float
    health_score: float  # 0 to 100
    volatility_7d: float
    is_paused: bool = False
    last_tx_anomaly_score: float = 0.0  # 0 to 1.0


@dataclass
class SentinelReport:
    timestamp: float
    threat_level: ThreatLevel
    anomaly_detected: AnomalyType
    compromised_strategies: List[str]
    confidence_score: float  # 0.0 - 1.0
    emergency_action_required: bool
    reasoning: str


@dataclass
class QuantAllocationPlan:
    timestamp: float
    target_allocations: Dict[str, float]  # strategy_address -> target percentage (0.0 - 1.0)
    expected_portfolio_apy: float
    expected_sharpe_ratio: float
    gas_cost_estimate_usd: float
    net_alpha_gain_usd: float
    explanation: str


@dataclass
class AuditorDecision:
    timestamp: float
    is_approved: bool
    violations: List[str]
    invariants_checked: Dict[str, bool]
    signed_intent_hash: Optional[str] = None


@dataclass
class AgentSystemState:
    vault_address: str
    total_aum_usd: float
    liquid_reserve_usd: float
    liquid_reserve_pct: float
    strategies: Dict[str, StrategyMetrics]
    latest_sentinel_report: Optional[SentinelReport] = None
    latest_quant_plan: Optional[QuantAllocationPlan] = None
    latest_auditor_decision: Optional[AuditorDecision] = None
    circuit_breaker_active: bool = False
    execution_history: List[Dict] = field(default_factory=list)
