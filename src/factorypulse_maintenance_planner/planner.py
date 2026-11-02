"""Deterministic maintenance triage, designed for human approval."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Iterable
from pathlib import Path
from typing import Any

from factorypulse_contracts import validate_event


def _recommendation_id(event: dict[str, Any]) -> str:
    key = f"{event['event_id']}|{event['asset_id']}|maintenance-review"
    return hashlib.sha256(key.encode()).hexdigest()[:16]


def _action(reasons: list[str]) -> str:
    text = " ".join(reasons).lower()
    if "vibration" in text:
        return "Inspect mechanical fastening, alignment and bearing condition."
    if "temperature" in text:
        return "Inspect cooling path, load and temperature sensor plausibility."
    return "Review the signal, operating context and asset history before intervention."


def plan(events: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    """Create one explainable, non-executing recommendation per anomaly event."""
    recommendations: list[dict[str, Any]] = []
    for event in events:
        validate_event("anomaly.v1", event)
        severity = event["severity"]
        recommendations.append(
            {
                "recommendation_id": _recommendation_id(event),
                "asset_id": event["asset_id"],
                "source_event_id": event["event_id"],
                "priority": "P1" if severity == "critical" else "P2",
                "recommended_within": "24h" if severity == "critical" else "5 business days",
                "action": _action(event["reasons"]),
                "rationale": event["reasons"],
                "status": "proposed",
                "approval_required": True,
                "safety_note": "A qualified person must review this proposal before any intervention.",
            }
        )
    return sorted(recommendations, key=lambda item: (item["priority"], item["recommendation_id"]))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_json(path: Path, recommendations: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(recommendations, indent=2, sort_keys=True) + "\n", encoding="utf-8")
