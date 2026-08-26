"""
Conformity Assessment Skeleton
------------------------------
Generates a mock technical documentation / conformity-style checklist
inspired by EU AI Act high-risk system expectations.
For portfolio and learning use only — not formal certification evidence.
"""

from __future__ import annotations

from typing import Any, Dict, List


def generate_conformity_checklist(use_case: Dict[str, Any], risk_result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Produce a structured checklist of typical technical documentation elements.
    """
    items: List[Dict[str, str]] = [
        {
            "id": "TD-01",
            "category": "General Description",
            "item": "Intended purpose, provider identity, and version of the AI system",
            "status": "DRAFT",
        },
        {
            "id": "TD-02",
            "category": "General Description",
            "item": "How the system interacts with hardware/software and external systems",
            "status": "DRAFT",
        },
        {
            "id": "TD-03",
            "category": "Design & Development",
            "item": "Design specifications, model overview, and key design choices",
            "status": "DRAFT",
        },
        {
            "id": "TD-04",
            "category": "Data Governance",
            "item": "Training / validation data characteristics, provenance, and quality measures",
            "status": "DRAFT",
        },
        {
            "id": "TD-05",
            "category": "Risk Management",
            "item": "Risk management system description and residual risk treatment",
            "status": "DRAFT",
        },
        {
            "id": "TD-06",
            "category": "Monitoring",
            "item": "Post-market / post-deployment monitoring plan and metrics",
            "status": "DRAFT",
        },
        {
            "id": "TD-07",
            "category": "Human Oversight",
            "item": "Human oversight measures and instructions for operators",
            "status": "DRAFT" if risk_result.get("hitl_recommended") else "N/A – review needed",
        },
        {
            "id": "TD-08",
            "category": "Accuracy & Robustness",
            "item": "Accuracy, robustness, and cybersecurity measures",
            "status": "DRAFT",
        },
        {
            "id": "TD-09",
            "category": "Logging",
            "item": "Automatic logging of relevant events for traceability",
            "status": "DRAFT",
        },
        {
            "id": "TD-10",
            "category": "Instructions for Use",
            "item": "Clear instructions for deployers / users including limitations",
            "status": "DRAFT",
        },
    ]

    if use_case.get("third_party_model"):
        items.append({
            "id": "TD-11",
            "category": "Third-Party Components",
            "item": "Documentation of third-party model / foundation model integration and responsibilities",
            "status": "DRAFT",
        })

    summary = {
        "applicable": risk_result.get("risk_level") in ("MEDIUM", "HIGH")
        or use_case.get("high_stakes_domain"),
        "note": (
            "This is a mock conformity-style checklist for learning and portfolio purposes. "
            "Formal conformity assessment under the EU AI Act requires qualified assessment "
            "and complete technical documentation."
        ),
        "checklist": items,
    }

    return summary
