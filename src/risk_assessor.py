"""
Risk Assessor
-------------
Produces a simple quantitative + qualitative risk score and flags
based on use-case characteristics.
"""

from __future__ import annotations

from typing import Any, Dict, List


def score_risk(use_case: Dict[str, Any]) -> Dict[str, Any]:
    """
    Lightweight scoring model (0–1). Higher = higher residual risk signal.
    This is a portfolio demonstration, not a certified risk methodology.
    """
    score = 0.15  # baseline

    if use_case.get("affects_individuals"):
        score += 0.20
    if use_case.get("automated_decision"):
        score += 0.15
    if use_case.get("high_stakes_domain"):
        score += 0.25
    if use_case.get("third_party_model"):
        score += 0.10
    if not use_case.get("human_in_the_loop_possible"):
        score += 0.15

    # Sector adjustments
    sector = use_case.get("sector", "")
    if sector in ("financial_services", "enterprise_automation"):
        score += 0.05

    score = min(round(score, 3), 1.0)

    # Qualitative level
    if score < 0.35:
        level = "LOW"
    elif score < 0.60:
        level = "MEDIUM"
    else:
        level = "HIGH"

    return {
        "risk_score": score,
        "risk_level": level,
    }


def generate_flags(use_case: Dict[str, Any], risk: Dict[str, Any]) -> List[str]:
    flags: List[str] = []

    if use_case.get("affects_individuals") and use_case.get("automated_decision"):
        flags.append("INDIVIDUAL_IMPACT_VIA_AUTOMATION")

    if use_case.get("high_stakes_domain"):
        flags.append("HIGH_STAKES_DOMAIN")

    if use_case.get("third_party_model"):
        flags.append("THIRD_PARTY_MODEL_SUPPLY_CHAIN")

    if use_case.get("human_in_the_loop_possible"):
        flags.append("HITL_FEASIBLE")
    else:
        flags.append("LIMITED_HUMAN_OVERSIGHT")

    if risk["risk_level"] == "HIGH":
        flags.append("ELEVATED_RESIDUAL_RISK")

    if not flags:
        flags.append("NO_MAJOR_FLAGS")

    return flags


def key_findings(use_case: Dict[str, Any], risk: Dict[str, Any], flags: List[str]) -> List[str]:
    findings: List[str] = []

    if "INDIVIDUAL_IMPACT_VIA_AUTOMATION" in flags:
        findings.append(
            "System can affect individuals through automated outputs or recommendations. "
            "Transparency and redress mechanisms should be considered."
        )

    if "HIGH_STAKES_DOMAIN" in flags:
        findings.append(
            "Operates in a higher-stakes domain. Recommend formal risk assessment, "
            "enhanced testing, and human review gates for consequential decisions."
        )

    if "THIRD_PARTY_MODEL_SUPPLY_CHAIN" in flags:
        findings.append(
            "Relies on a third-party model provider. Perform due diligence on data handling, "
            "security, sub-processors, and contractual AI terms."
        )

    if "HITL_FEASIBLE" in flags:
        findings.append(
            "Human-in-the-loop (HITL) is feasible. Design clear escalation paths and "
            "document override criteria for high-impact cases."
        )

    if "ELEVATED_RESIDUAL_RISK" in flags:
        findings.append(
            "Composite risk signal is elevated. Prioritise DPIA, monitoring plan, "
            "and periodic re-evaluation under NIST AI RMF Manage function."
        )

    findings.append(
        "Map residual risks to NIST AI RMF (Govern/Map/Measure/Manage), "
        "EU AI Act transparency & oversight expectations, and ISO/IEC 42001 monitoring evidence."
    )

    return findings


def assess(use_case: Dict[str, Any]) -> Dict[str, Any]:
    risk = score_risk(use_case)
    flags = generate_flags(use_case, risk)
    findings = key_findings(use_case, risk, flags)

    return {
        **risk,
        "risk_flags": flags,
        "key_findings": findings,
        "hitl_recommended": bool(use_case.get("human_in_the_loop_possible"))
        and (use_case.get("affects_individuals") or use_case.get("high_stakes_domain")),
        "dpia_recommended": bool(
            use_case.get("affects_individuals")
            and (use_case.get("automated_decision") or use_case.get("high_stakes_domain"))
        ),
    }
