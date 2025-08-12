from typing import List

from .schemas import IssuePrediction, PredictionResponse, ReadingInput


def clamp(value: float, min_value: float, max_value: float) -> float:
    return max(min_value, min(max_value, value))


def score_to_severity(prob: float) -> str:
    if prob >= 0.75:
        return "high"
    if prob >= 0.4:
        return "medium"
    return "low"


def predict_health(reading: ReadingInput) -> PredictionResponse:
    issues: List[IssuePrediction] = []

    # Battery health heuristic
    battery_prob = 0.0
    recommendation_battery = ""
    if reading.battery_voltage_v is not None:
        if reading.battery_voltage_v < 11.8:
            battery_prob = 0.85
            recommendation_battery = (
                "Battery voltage is low. Check terminals, test battery, consider replacement."
            )
        elif reading.battery_voltage_v < 12.2:
            battery_prob = 0.45
            recommendation_battery = (
                "Battery may be weakening. Charge fully and re-test; inspect alternator."
            )
    elif reading.symptoms and any("hard start" in s.lower() or "click" in s.lower() for s in reading.symptoms):
        battery_prob = 0.4
        recommendation_battery = "Possible weak battery based on symptoms. Test battery and charging system."

    if battery_prob > 0:
        issues.append(
            IssuePrediction(
                issue_type="battery",
                probability=battery_prob,
                severity=score_to_severity(battery_prob),
                recommendation=recommendation_battery or "Test battery and charging system.",
            )
        )

    # Overheating heuristic
    overheat_prob = 0.0
    recommendation_overheat = ""
    if reading.coolant_temp_c is not None:
        if reading.coolant_temp_c >= 110:
            overheat_prob = 0.9
            recommendation_overheat = (
                "High coolant temperature. Stop vehicle, check coolant level, fans, and thermostat."
            )
        elif reading.coolant_temp_c >= 100:
            overheat_prob = 0.5
            recommendation_overheat = (
                "Coolant temperature elevated. Inspect coolant, radiator, and airflow."
            )
    elif reading.symptoms and any("overheat" in s.lower() for s in reading.symptoms):
        overheat_prob = 0.4
        recommendation_overheat = "Reported overheating. Inspect coolant and radiator."

    if overheat_prob > 0:
        issues.append(
            IssuePrediction(
                issue_type="engine_overheating",
                probability=overheat_prob,
                severity=score_to_severity(overheat_prob),
                recommendation=recommendation_overheat or "Inspect cooling system.",
            )
        )

    # Brake wear heuristic (mileage + last service)
    brake_prob = 0.0
    recommendation_brake = ""
    mileage = reading.mileage_km or 0.0
    last_service = reading.last_service_km_ago or 0.0
    if mileage > 40000 and last_service > 15000:
        brake_prob = 0.6
        recommendation_brake = (
            "High mileage since service. Inspect brake pads, discs/drums, and fluid."
        )
    elif last_service > 25000:
        brake_prob = 0.8
        recommendation_brake = "Very long interval since brake service. Service recommended."
    elif reading.symptoms and any("squeal" in s.lower() or "grind" in s.lower() for s in reading.symptoms):
        brake_prob = 0.7
        recommendation_brake = "Brake noise reported. Inspect pads/rotors immediately."

    if brake_prob > 0:
        issues.append(
            IssuePrediction(
                issue_type="brake_wear",
                probability=brake_prob,
                severity=score_to_severity(brake_prob),
                recommendation=recommendation_brake or "Brake inspection recommended.",
            )
        )

    # Tire pressure heuristic
    tire_prob = 0.0
    recommendation_tire = ""
    if reading.tire_pressures_psi:
        avg_psi = sum(reading.tire_pressures_psi) / len(reading.tire_pressures_psi)
        min_psi = min(reading.tire_pressures_psi)
        max_psi = max(reading.tire_pressures_psi)
        if max_psi - min_psi >= 6:
            tire_prob = 0.5
            recommendation_tire = "Uneven tire pressures. Balance to manufacturer spec to avoid wear."
        if avg_psi < 28:
            tire_prob = max(tire_prob, 0.7)
            recommendation_tire = (
                recommendation_tire or "Low tire pressure. Inflate to recommended PSI."
            )

    if tire_prob > 0:
        issues.append(
            IssuePrediction(
                issue_type="tire_pressure",
                probability=tire_prob,
                severity=score_to_severity(tire_prob),
                recommendation=recommendation_tire or "Check and adjust tire pressures.",
            )
        )

    # Compute health score: penalize by weighted issue probabilities
    weights = {
        "battery": 30,
        "engine_overheating": 35,
        "brake_wear": 25,
        "tire_pressure": 10,
    }
    penalty = 0.0
    for issue in issues:
        penalty += weights.get(issue.issue_type, 10) * issue.probability

    raw_score = 100.0 - penalty
    health_score = clamp(raw_score, 0.0, 100.0)

    notes = None
    if not issues:
        notes = "No obvious issues detected from provided inputs."

    return PredictionResponse(health_score=health_score, issues=issues, notes=notes)