from typing import Optional, List
from pydantic import BaseModel, Field


class FlightInfo(BaseModel):
    flight_number: str
    departure_airport: str
    arrival_airport: str
    departure_time: str
    carrier: Optional[str] = None
    weather_alert_level: Optional[int] = Field(default=0, ge=0, le=3)
    historical_delay_index: Optional[float] = Field(default=0.0, ge=0.0, le=1.0)
    airport_congestion_level: Optional[float] = Field(default=0.0, ge=0.0, le=1.0)
    crew_shortage_risk: Optional[float] = Field(default=0.0, ge=0.0, le=1.0)
    atc_delay_risk: Optional[float] = Field(default=0.0, ge=0.0, le=1.0)
    maintenance_risk: Optional[float] = Field(default=0.0, ge=0.0, le=1.0)


class PredictionRequest(BaseModel):
    flight_info: FlightInfo


class AlternativesRequest(BaseModel):
    flight_info: FlightInfo


class NotifyRequest(BaseModel):
    message: str
    webhook_url: Optional[str] = None


class AgentRunRequest(BaseModel):
    flight_info: FlightInfo


class PredictionResult(BaseModel):
    risk_score: float
    risk_level: str
    contributing_factors: List[str]
    threshold: float

