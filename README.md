# FactoryPulse Maintenance Planner

An explainable, deterministic component that translates validated FactoryPulse anomaly events into maintenance recommendations for human review.

It is deliberately a recommendation layer, not a CMMS replacement, scheduler or equipment-control tool. Every output has `status: proposed`, retains its source event and requires approval.

## What it does

1. Validates each input against the versioned `anomaly.v1` contract.
2. Assigns a transparent priority and recommended response window.
3. Maps signal evidence to an inspection-oriented action.
4. Produces JSON suitable for review or a later CMMS integration.

## Quick start

```bash
pip install .
factorypulse-plan-maintenance anomalies.jsonl --output maintenance_recommendations.json
```

## Example output

```json
{
  "priority": "P1",
  "recommended_within": "24h",
  "status": "proposed",
  "approval_required": true
}
```

The recommendation includes the original anomaly id and rationale. It never instructs a control system or represents a safety decision.

## Development

```bash
pip install ".[dev]"
pytest -q
```

## Scope

Reference software for learning, evaluation and internal integration. Maintenance and safety decisions require qualified personnel, local procedures and a suitable management system.

## License

MIT
