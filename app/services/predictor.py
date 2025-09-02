import os
from typing import Dict, List
from app.schemas.models import FlightInfo, PredictionResult


class PredictorService:
    def __init__(self):
        self.risk_threshold = float(os.getenv("RISK_THRESHOLD", "0.6"))

    def predict(self, flight_info: FlightInfo) -> PredictionResult:
        # Simple interpretable baseline: weighted sum of risk contributors
        weights: Dict[str, float] = {
            "weather_alert_level": 0.25,
            "historical_delay_index": 0.2,
            "airport_congestion_level": 0.2,
            "crew_shortage_risk": 0.15,
            "atc_delay_risk": 0.15,
            "maintenance_risk": 0.05,
        }

        # Normalize weather alert (0-3) to 0-1
        weather_norm = min(max((flight_info.weather_alert_level or 0) / 3.0, 0.0), 1.0)

        risk_score = (
            weights["weather_alert_level"] * weather_norm
            + weights["historical_delay_index"] * (flight_info.historical_delay_index or 0.0)
            + weights["airport_congestion_level"] * (flight_info.airport_congestion_level or 0.0)
            + weights["crew_shortage_risk"] * (flight_info.crew_shortage_risk or 0.0)
            + weights["atc_delay_risk"] * (flight_info.atc_delay_risk or 0.0)
            + weights["maintenance_risk"] * (flight_info.maintenance_risk or 0.0)
        )

        factors: List[str] = []
        if weather_norm > 0.5:
            factors.append("Adverse weather conditions")
        if (flight_info.historical_delay_index or 0.0) > 0.5:
            factors.append("Poor historical on-time performance")
        if (flight_info.airport_congestion_level or 0.0) > 0.5:
            factors.append("High airport congestion")
        if (flight_info.crew_shortage_risk or 0.0) > 0.5:
            factors.append("Crew shortage risk")
        if (flight_info.atc_delay_risk or 0.0) > 0.5:
            factors.append("ATC delays expected")
        if (flight_info.maintenance_risk or 0.0) > 0.5:
            factors.append("Maintenance-related delays")

        risk_level = "high" if risk_score >= self.risk_threshold else "low"
        return PredictionResult(
            risk_score=risk_score,
            risk_level=risk_level,
            contributing_factors=factors,
            threshold=self.risk_threshold,
        )

