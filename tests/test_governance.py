"""
Unit tests for AIGP Governance Toolkit.
"""

from __future__ import annotations

import pytest

from src.frameworks import list_use_cases, get_use_case, full_framework_map, USE_CASES
from src.risk_assessor import assess, score_risk
from src.dpia import generate_dpia
from src.conformity import generate_conformity_checklist
from src.reports import build_full_assessment


def test_list_use_cases_not_empty():
    keys = list_use_cases()
    assert len(keys) >= 3
    assert "enterprise_llm_support_agent" in keys


def test_get_use_case_valid():
    uc = get_use_case("credit_risk_scoring")
    assert uc["name"]
    assert uc["high_stakes_domain"] is True


def test_get_use_case_invalid():
    with pytest.raises(KeyError):
        get_use_case("nonexistent_use_case_xyz")


def test_score_risk_high_for_credit():
    uc = get_use_case("credit_risk_scoring")
    result = score_risk(uc)
    assert result["risk_score"] >= 0.5
    assert result["risk_level"] in ("MEDIUM", "HIGH")


def test_score_risk_lower_for_internal_tool():
    uc = get_use_case("internal_code_assistant")
    result = score_risk(uc)
    assert result["risk_score"] < score_risk(get_use_case("credit_risk_scoring"))["risk_score"]


def test_assess_returns_expected_keys():
    uc = get_use_case("enterprise_llm_support_agent")
    result = assess(uc)
    for key in ("risk_score", "risk_level", "risk_flags", "key_findings", "hitl_recommended", "dpia_recommended"):
        assert key in result


def test_dpia_structure():
    uc = get_use_case("agentic_workflow_orchestrator")
    risk = assess(uc)
    dpia = generate_dpia(uc, risk)
    assert "title" in dpia
    assert "risks_to_rights_and_freedoms" in dpia
    assert "mitigating_measures" in dpia
    assert isinstance(dpia["mitigating_measures"], list)


def test_conformity_checklist_has_items():
    uc = get_use_case("credit_risk_scoring")
    risk = assess(uc)
    conf = generate_conformity_checklist(uc, risk)
    assert "checklist" in conf
    assert len(conf["checklist"]) >= 8


def test_full_framework_map():
    result = full_framework_map("enterprise_llm_support_agent")
    assert "nist_ai_rmf" in result
    assert "eu_ai_act" in result
    assert "iso_42001" in result
    assert set(result["nist_ai_rmf"].keys()) == {"Govern", "Map", "Measure", "Manage"}


def test_end_to_end_assessment_build():
    key = "enterprise_llm_support_agent"
    fmap = full_framework_map(key)
    risk = assess(fmap["use_case"])
    dpia = generate_dpia(fmap["use_case"], risk)
    conf = generate_conformity_checklist(fmap["use_case"], risk)
    assessment = build_full_assessment(key, fmap, risk, dpia, conf)

    assert assessment["use_case_key"] == key
    assert "risk" in assessment
    assert "dpia" in assessment
    assert "conformity_checklist" in assessment
    assert "disclaimer" in assessment
