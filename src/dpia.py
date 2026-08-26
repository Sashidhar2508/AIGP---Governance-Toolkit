"""
DPIA Draft Generator
--------------------
Produces a structured Data Protection Impact Assessment outline
suitable for portfolio demonstration and internal discussion.
Not a substitute for formal legal advice.
"""

from __future__ import annotations

from typing import Any, Dict, List


def generate_dpia(use_case: Dict[str, Any], risk_result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Build a DPIA-style structured document.
    """
    name = use_case.get("name", "Unnamed AI System")
    description = use_case.get("description", "")
    data_cats = use_case.get("data_categories", [])

    necessity = (
        "The processing is considered necessary for the stated legitimate interest / "
        "contractual purpose of delivering the AI-enabled service. Alternatives "
        "(fully manual processes) may be less efficient or scalable."
    )

    proportionality = (
        "Data minimisation and purpose limitation principles should be applied. "
        "Only categories required for the use case should be retained, with clear retention schedules."
    )

    risks_to_rights = []
    if use_case.get("affects_individuals"):
        risks_to_rights.append("Potential impact on individuals’ rights and freedoms via automated outputs or decisions.")
    if use_case.get("automated_decision"):
        risks_to_rights.append("Risk of opaque or insufficiently explainable automated processing.")
    if use_case.get("high_stakes_domain"):
        risks_to_rights.append("Higher severity of impact if errors or bias occur in a high-stakes context.")
    if use_case.get("third_party_model"):
        risks_to_rights.append("Third-party model processing may involve additional international transfers or sub-processors.")

    if not risks_to_rights:
        risks_to_rights.append("Limited direct impact on individuals identified under current description.")

    measures: List[str] = [
        "Document intended purpose and lawful basis",
        "Apply data minimisation and retention limits",
        "Implement access controls and logging",
        "Provide transparency notice to affected individuals where required",
    ]

    if risk_result.get("hitl_recommended"):
        measures.append("Human-in-the-loop review for high-impact or edge-case decisions")

    if use_case.get("third_party_model"):
        measures.append("Contractual clauses and due diligence on model provider (security, sub-processors, data use)")

    if risk_result.get("dpia_recommended"):
        measures.append("Periodic re-assessment of residual risk and effectiveness of controls")

    return {
        "title": f"DPIA Draft – {name}",
        "system_description": description,
        "data_categories": data_cats,
        "necessity": necessity,
        "proportionality": proportionality,
        "risks_to_rights_and_freedoms": risks_to_rights,
        "mitigating_measures": measures,
        "dpia_required_indicator": risk_result.get("dpia_recommended", False),
        "residual_risk_level": risk_result.get("risk_level", "UNKNOWN"),
        "consultation_notes": (
            "Consult DPO / privacy counsel and relevant business owners before finalising. "
            "This draft is generated for portfolio and discussion purposes only."
        ),
    }
