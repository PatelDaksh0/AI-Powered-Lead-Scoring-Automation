# VehicleGuard — MVP

A user-friendly vehicle health predictor for everyday users. Cross-platform mobile (React Native/Expo) with a Python (FastAPI) backend. MVP focuses on manual inputs and basic predictions for cars and bikes.

## Architecture (MVP)
- Frontend: React Native (Expo). Manual inputs, simple results screens.
- Backend: FastAPI (Python). Rule-based predictor (extensible to ML/Scikit-learn).
- Data: In-memory (MVP). Replace with SQLite/Postgres later.

## Quickstart (Backend)
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Open API docs: http://localhost:8000/docs

### Example: Predict
```bash
curl -X POST http://localhost:8000/predict \
  -H 'Content-Type: application/json' \
  -d '{
    "vehicle_type": "car",
    "mileage_km": 60000,
    "last_service_km_ago": 16000,
    "battery_voltage_v": 11.7,
    "coolant_temp_c": 108,
    "tire_pressures_psi": [28,30,31,29],
    "symptoms": ["engine_rattling"]
  }'
```

## Quickstart (Mobile - stub)
- Ensure backend is running on your machine/network.
- Update `mobile/src/config.ts` `API_BASE_URL` if needed.
- Run with Expo (if you have Node/Expo):
```bash
cd mobile
npm install
npm start
```

## MVP Scope
- Manual inputs: mileage, last service, battery voltage, coolant temp, tire pressure, symptoms.
- Predictions: health score + issue probabilities (battery, brakes, overheating) with recommendations.
- No auth; single user, multi-vehicle later.

## Roadmap (high-level)
- Week 1–2: MVP backend + forms + results.
- Week 3–4: History, basic charts, image/noise input capture (no ML).
- Month 2–3: OBD-II adapter integration (where available), simple ML model.
- Month 6+: Fleet, wearables/GPS integration, premium features.

## License
MIT (placeholder).

