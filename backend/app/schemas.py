from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class VehicleType(str, Enum):
    car = "car"
    bike = "bike"
    scooter = "scooter"
    truck = "truck"


class ReadingInput(BaseModel):
    vehicle_type: VehicleType = Field(description="Type of vehicle")
    mileage_km: Optional[float] = Field(default=None, ge=0)
    last_service_km_ago: Optional[float] = Field(default=None, ge=0)
    battery_voltage_v: Optional[float] = Field(default=None, ge=0)
    coolant_temp_c: Optional[float] = Field(default=None)
    tire_pressures_psi: Optional[List[float]] = None
    fuel_efficiency_kmpl: Optional[float] = Field(default=None, ge=0)
    symptoms: Optional[List[str]] = Field(default_factory=list)


class IssuePrediction(BaseModel):
    issue_type: str
    probability: float = Field(ge=0.0, le=1.0)
    severity: str = Field(description="low | medium | high")
    recommendation: str


class PredictionResponse(BaseModel):
    health_score: float = Field(ge=0.0, le=100.0)
    issues: List[IssuePrediction]
    notes: Optional[str] = None