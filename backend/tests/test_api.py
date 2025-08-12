from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_predict_basic():
    payload = {
        "vehicle_type": "car",
        "mileage_km": 60000,
        "last_service_km_ago": 16000,
        "battery_voltage_v": 11.7,
        "coolant_temp_c": 108,
        "tire_pressures_psi": [28, 30, 31, 29],
        "symptoms": ["engine_rattling"],
    }
    resp = client.post("/predict", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert "health_score" in data
    assert 0 <= data["health_score"] <= 100
    assert isinstance(data.get("issues"), list)
    assert any(i["issue_type"] == "battery" for i in data["issues"])  # low voltage