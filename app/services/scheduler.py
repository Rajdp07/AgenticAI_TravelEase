import os
from typing import Dict, Any
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from app.services.agent import AgentService
from app.schemas.models import FlightInfo


class MonitorScheduler:
    def __init__(self, agent: AgentService):
        self.agent = agent
        self.scheduler = BackgroundScheduler()
        self.tracked: Dict[str, Dict[str, Any]] = {}

    def start(self):
        if os.getenv("SCHEDULER_ENABLED", "false").lower() == "true":
            interval_seconds = int(os.getenv("SCHEDULER_INTERVAL_SECONDS", "300"))
            self.scheduler.add_job(self._tick, IntervalTrigger(seconds=interval_seconds))
            self.scheduler.start()

    def subscribe(self, key: str, flight_info: FlightInfo):
        self.tracked[key] = {"flight_info": flight_info}

    def unsubscribe(self, key: str):
        self.tracked.pop(key, None)

    def _tick(self):
        for key, item in list(self.tracked.items()):
            try:
                self.agent.run(item["flight_info"])
            except Exception:
                pass

