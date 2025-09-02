from datetime import datetime, timedelta
from typing import List, Dict
from app.schemas.models import FlightInfo


class AlternativesService:
    def suggest(self, flight_info: FlightInfo) -> List[Dict]:
        # Mocked suggestions. A real implementation would query GDS/NDC or provider APIs.
        dt = datetime.fromisoformat(flight_info.departure_time.replace("Z", "+00:00"))
        results = [
            {
                "type": "reroute",
                "carrier": flight_info.carrier or "XY",
                "flight_number": f"{(flight_info.carrier or 'XY')}987",
                "departure_airport": flight_info.departure_airport,
                "arrival_airport": flight_info.arrival_airport,
                "departure_time": (dt + timedelta(hours=2)).isoformat(),
                "stops": 0,
                "reason": "Later departure to avoid weather window",
                "score": 0.78,
            },
            {
                "type": "connect",
                "carrier": flight_info.carrier or "XY",
                "flight_number": f"{(flight_info.carrier or 'XY')}456",
                "departure_airport": flight_info.departure_airport,
                "connection_airport": "ORD",
                "arrival_airport": flight_info.arrival_airport,
                "departure_time": (dt + timedelta(hours=3)).isoformat(),
                "stops": 1,
                "reason": "Alternative routing via less congested hub",
                "score": 0.72,
            },
            {
                "type": "nearby_airport",
                "carrier": flight_info.carrier or "XY",
                "flight_number": f"{(flight_info.carrier or 'XY')}321",
                "departure_airport": "EWR" if flight_info.departure_airport == "JFK" else flight_info.departure_airport,
                "arrival_airport": flight_info.arrival_airport,
                "departure_time": (dt + timedelta(hours=1)).isoformat(),
                "stops": 0,
                "reason": "Depart from nearby airport with lower ATC delays",
                "score": 0.65,
            },
        ]
        # Sort by score descending
        results.sort(key=lambda x: x.get("score", 0), reverse=True)
        return results

