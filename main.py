#!/usr/bin/env python3
"""
AIGP Governance Toolkit — CLI Entry Point
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from src.frameworks import full_framework_map, list_use_cases
from src.risk_assessor import assess
from src.dpia import generate_dpia
from src.conformity import generate_conformity_checklist
from src.reports import build_full_assessment, export_all


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Enterprise AI risk, DPIA & conformity toolkit for AIGP / governance practitioners",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--use-case",
        type=str,
        default="enterprise_llm_support_agent",
        help="Key of the demo use case to assess",
    )
    parser.add_argument(
        "--list-use-cases",
        action="store_true",
        help="List available demo use cases and exit",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="examples/sample_assessment",
        help="Output path stem (without extension) for JSON + Markdown reports",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.list_use_cases:
        print("Available demo use cases:")
        for key in list_use_cases():
            print(f"  • {key}")
        return

    print(f"[*] Loading use case: {args.use_case}")
    framework_map = full_framework_map(args.use_case)
    use_case = framework_map["use_case"]

    print("[*] Running risk assessment …")
    risk_result = assess(use_case)

    print("[*] Generating DPIA draft …")
    dpia = generate_dpia(use_case, risk_result)

    print("[*] Building conformity-style checklist …")
    conformity = generate_conformity_checklist(use_case, risk_result)

    print("[*] Assembling full evidence pack …")
    assessment = build_full_assessment(
        use_case_key=args.use_case,
        framework_map=framework_map,
        risk_result=risk_result,
        dpia=dpia,
        conformity=conformity,
    )

    paths = export_all(assessment, args.output)

    print("\n=== Assessment Summary ===")
    print(f"  Use Case     : {use_case.get('name')}")
    print(f"  Risk Score   : {risk_result['risk_score']} ({risk_result['risk_level']})")
    print(f"  DPIA Rec.    : {risk_result['dpia_recommended']}")
    print(f"  HITL Rec.    : {risk_result['hitl_recommended']}")
    print(f"  EU Tier Hint : {framework_map['eu_ai_act']['tier_hint']}")
    print(f"  Reports      :")
    for kind, p in paths.items():
        print(f"    - {kind:8s} → {p}")
    print("==========================\n")


if __name__ == "__main__":
    main()
