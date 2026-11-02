from factorypulse_maintenance_planner.planner import plan


def anomaly(*, severity: str = "critical", reasons: list[str] | None = None) -> dict[str, object]:
    return {
        "event_id": "123e4567-e89b-12d3-a456-426614174000",
        "event_type": "factorypulse.anomaly",
        "schema_version": "1.0",
        "occurred_at": "2026-01-01T12:00:00Z",
        "asset_id": "PUMP-01",
        "severity": severity,
        "score": 6.2,
        "reasons": reasons or ["vibration critical (9.1 mm/s)"],
    }


def test_critical_vibration_produces_a_safe_prioritized_proposal() -> None:
    recommendation = plan([anomaly()])[0]
    assert recommendation["priority"] == "P1"
    assert recommendation["status"] == "proposed"
    assert recommendation["approval_required"] is True
    assert "bearing" in recommendation["action"]


def test_temperature_uses_relevant_inspection_guidance() -> None:
    recommendation = plan([anomaly(severity="warning", reasons=["temperature critical (92.1 C)"])])[0]
    assert recommendation["priority"] == "P2"
    assert "cooling" in recommendation["action"]
