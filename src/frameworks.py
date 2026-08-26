"""
Framework Mapper
----------------
Maps AI system characteristics to NIST AI RMF functions,
EU AI Act risk considerations, and ISO/IEC 42001 concepts.
"""

from __future__ import annotations

from typing import Any, Dict, List


# Demo catalog of use cases (extendable)
USE_CASES: Dict[str, Dict[str, Any]] = {
    "enterprise_llm_support_agent": {
        "name": "Enterprise LLM Customer Support Agent",
        "description": "LLM-powered agent assisting customers with product and billing queries, with escalation to human agents.",
        "data_categories": ["customer_contact", "transaction_history", "support_tickets"],
        "automated_decision": True,
        "affects_individuals": True,
        "high_stakes_domain": False,
        "third_party_model": True,
        "human_in_the_loop_possible": True,
        "sector": "general_enterprise",
    },
    "credit_risk_scoring": {
        "name": "Automated Credit Risk Scoring",
        "description": "ML model producing credit risk scores used in lending decisions.",
        "data_categories": ["financial", "personal_identifiers", "credit_history"],
        "automated_decision": True,
        "affects_individuals": True,
        "high_stakes_domain": True,
        "third_party_model": False,
        "human_in_the_loop_possible": True,
        "sector": "financial_services",
    },
    "internal_code_assistant": {
        "name": "Internal Developer Code Assistant",
        "description": "LLM coding assistant used only by internal engineering teams on non-sensitive codebases.",
        "data_categories": ["source_code", "internal_docs"],
        "automated_decision": False,
        "affects_individuals": False,
        "high_stakes_domain": False,
        "third_party_model": True,
        "human_in_the_loop_possible": True,
        "sector": "internal_tools",
    },
    "agentic_workflow_orchestrator": {
        "name": "Agentic Multi-Step Workflow Orchestrator",
        "description": "Autonomous agent chain that plans and executes multi-step business processes with tool use.",
        "data_categories": ["business_process_data", "customer_records", "system_logs"],
        "automated_decision": True,
        "affects_individuals": True,
        "high_stakes_domain": True,
        "third_party_model": True,
        "human_in_the_loop_possible": True,
        "sector": "enterprise_automation",
    },
}


def list_use_cases() -> List[str]:
    return list(USE_CASES.keys())


def get_use_case(key: str) -> Dict[str, Any]:
    if key not in USE_CASES:
        raise KeyError(f"Unknown use case '{key}'. Available: {list_use_cases()}")
    return USE_CASES[key].copy()


def map_nist_rmf(use_case: Dict[str, Any]) -> Dict[str, List[str]]:
    """
    Return suggested NIST AI RMF activities per function.
    """
    mapping = {
        "Govern": [
            "Define AI risk tolerance and accountability",
            "Establish roles for AI oversight and escalation",
            "Document third-party model / provider governance",
        ],
        "Map": [
            "Inventory AI system context, intended use, and stakeholders",
            "Identify data categories and potential harms",
            "Classify risk level based on impact and domain",
        ],
        "Measure": [
            "Define metrics for performance, fairness, drift, and robustness",
            "Implement monitoring of outputs and decision outcomes",
            "Track human override / escalation rates where HITL exists",
        ],
        "Manage": [
            "Implement risk treatments (controls, HITL gates, fallbacks)",
            "Plan incident response and model rollback procedures",
            "Schedule periodic re-evaluation and continual improvement",
        ],
    }

    # Contextual additions
    if use_case.get("third_party_model"):
        mapping["Govern"].append("Due diligence on model provider security & data handling")
        mapping["Map"].append("Map supply-chain / third-party risk surface")

    if use_case.get("high_stakes_domain"):
        mapping["Measure"].append("Heightened fairness and disparate impact testing")
        mapping["Manage"].append("Mandatory human review for high-impact decisions")

    return mapping


def map_eu_ai_act_signals(use_case: Dict[str, Any]) -> Dict[str, Any]:
    """
    Lightweight EU AI Act style signals (not formal legal classification).
    """
    risk_signals = []
    tier_hint = "MINIMAL"

    if use_case.get("affects_individuals") and use_case.get("automated_decision"):
        risk_signals.append("Potential impact on individuals via automated outputs")
        tier_hint = "LIMITED"

    if use_case.get("high_stakes_domain"):
        risk_signals.append("Operates in a higher-stakes domain (e.g., finance, critical decisions)")
        tier_hint = "HIGH (contextual – requires formal assessment)"

    if use_case.get("third_party_model"):
        risk_signals.append("Relies on third-party foundation / frontier model")

    obligations = [
        "Transparency to users that they are interacting with AI (where applicable)",
        "Technical documentation and logging of system behaviour",
        "Human oversight mechanisms for higher-risk scenarios",
    ]

    if tier_hint.startswith("HIGH"):
        obligations.extend([
            "Formal risk management system",
            "Data governance and quality management",
            "Conformity assessment style technical file (mock in this toolkit)",
        ])

    return {
        "tier_hint": tier_hint,
        "risk_signals": risk_signals,
        "suggested_obligations": obligations,
    }


def map_iso_42001(use_case: Dict[str, Any]) -> List[str]:
    """
    High-level ISO/IEC 42001 style management system evidence points.
    """
    items = [
        "AI policy and scope definition",
        "Risk assessment and treatment records",
        "Competence and awareness of AI roles",
        "Operational planning and control of AI systems",
        "Performance evaluation (monitoring, measurement, audit)",
        "Continual improvement and management review",
    ]
    if use_case.get("third_party_model"):
        items.append("Supplier / third-party AI control and monitoring")
    return items


def full_framework_map(use_case_key: str) -> Dict[str, Any]:
    uc = get_use_case(use_case_key)
    return {
        "use_case_key": use_case_key,
        "use_case": uc,
        "nist_ai_rmf": map_nist_rmf(uc),
        "eu_ai_act": map_eu_ai_act_signals(uc),
        "iso_42001": map_iso_42001(uc),
    }
