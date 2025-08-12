# VehicleGuard PRD (MVP)

## Problem
Users lack accessible tools to understand vehicle health and prevent breakdowns.

## Goal
Predict likely issues and provide clear actions via a friendly mobile interface.

## Users
- Commuters, delivery riders, hobbyists.

## MVP Features
- Manual input: mileage, last service, battery voltage, coolant temp, tire pressures, symptoms.
- Output: health score, top issues (battery, brakes, overheating, tires), recommendations.
- History/logs: out of scope for MVP.
- Auth: out of scope for MVP.

## Non-Goals
- OBD-II integration, community, image/noise ML, fleet dashboard.

## Success Metrics
- Time-to-first-prediction < 30s.
- User comprehension (self-reported) > 80%.

## Risks & Mitigations
- Inaccurate inputs → guided hints, unit validation, ranges.
- Overtrust in output → confidence ranges, recommendations with caution notes.

## Future
- OBD-II auto data, basic ML (scikit-learn), image/noise analysis, offline-first, fleet features.