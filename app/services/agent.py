from typing import Dict, Any
from app.schemas.models import FlightInfo
from app.services.predictor import PredictorService
from app.services.alternatives import AlternativesService
from app.services.notifier import NotifierService


class AgentService:
    def __init__(self, predictor: PredictorService, alternatives: AlternativesService, notifier: NotifierService):
        self.predictor = predictor
        self.alternatives = alternatives
        self.notifier = notifier

    def run(self, flight_info: FlightInfo) -> Dict[str, Any]:
        prediction = self.predictor.predict(flight_info)
        alternatives = []
        notification_message = None

        if prediction.risk_level == "high":
            alternatives = self.alternatives.suggest(flight_info)
            notification_message = (
                f"High disruption risk for {flight_info.flight_number} "
                f"({flight_info.departure_airport}->{flight_info.arrival_airport}) "
                f"score={prediction.risk_score:.2f}. Alternatives suggested: {len(alternatives)}"
            )
            self.notifier.notify(notification_message)
        else:
            notification_message = (
                f"Low disruption risk for {flight_info.flight_number}. No action needed."
            )
            self.notifier.notify(notification_message)

        return {
            "prediction": prediction.model_dump(),
            "alternatives": alternatives,
            "notified": True,
            "message": notification_message,
        }

