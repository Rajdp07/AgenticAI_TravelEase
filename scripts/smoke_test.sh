#!/usr/bin/env bash
set -euo pipefail

API_URL=${API_URL:-http://localhost:8000}

filter_json() {
  if command -v jq >/dev/null 2>&1; then
    jq .
  else
    cat
  fi
}

echo "[1/4] Health check"
curl -s "$API_URL/health" | filter_json

echo "[2/4] Predict"
curl -s -X POST "$API_URL/predict" \
  -H 'Content-Type: application/json' \
  -d '{
    "flight_info": {
      "flight_number": "XY123",
      "departure_airport": "JFK",
      "arrival_airport": "LAX",
      "departure_time": "2025-09-02T12:00:00Z",
      "carrier": "XY",
      "weather_alert_level": 1,
      "historical_delay_index": 0.2,
      "airport_congestion_level": 0.4,
      "crew_shortage_risk": 0.1,
      "atc_delay_risk": 0.2,
      "maintenance_risk": 0.05
    }
  }' | filter_json

echo "[3/4] Alternatives"
curl -s -X POST "$API_URL/alternatives" \
  -H 'Content-Type: application/json' \
  -d '{
    "flight_info": {
      "flight_number": "XY123",
      "departure_airport": "JFK",
      "arrival_airport": "LAX",
      "departure_time": "2025-09-02T12:00:00Z",
      "carrier": "XY",
      "weather_alert_level": 0,
      "historical_delay_index": 0.1,
      "airport_congestion_level": 0.3,
      "crew_shortage_risk": 0.1,
      "atc_delay_risk": 0.1,
      "maintenance_risk": 0.05
    }
  }' | filter_json

echo "[4/4] Agent run"
curl -s -X POST "$API_URL/agent/run" \
  -H 'Content-Type: application/json' \
  -d '{
    "flight_info": {
      "flight_number": "XY123",
      "departure_airport": "JFK",
      "arrival_airport": "LAX",
      "departure_time": "2025-09-02T12:00:00Z",
      "carrier": "XY",
      "weather_alert_level": 2,
      "historical_delay_index": 0.4,
      "airport_congestion_level": 0.5,
      "crew_shortage_risk": 0.2,
      "atc_delay_risk": 0.3,
      "maintenance_risk": 0.1
    }
  }' | filter_json

echo "Done."
