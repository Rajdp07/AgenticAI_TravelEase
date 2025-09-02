from typing import Optional
from fastapi import APIRouter
from app.schemas.models import FlightInfo
from app.services.scheduler import MonitorScheduler
from app.services.agent import AgentService


router = APIRouter()

_agent_ref: Optional[AgentService] = None
_scheduler_ref: Optional[MonitorScheduler] = None


def init_scheduler(agent: AgentService):
    global _agent_ref, _scheduler_ref
    _agent_ref = agent
    _scheduler_ref = MonitorScheduler(agent)
    _scheduler_ref.start()


@router.post("/monitor/subscribe")
def subscribe(flight_info: FlightInfo):
    assert _scheduler_ref is not None
    key = f"{flight_info.flight_number}:{flight_info.departure_time}"
    _scheduler_ref.subscribe(key, flight_info)
    return {"status": "subscribed", "key": key}


@router.post("/monitor/unsubscribe")
def unsubscribe(key: str):
    assert _scheduler_ref is not None
    _scheduler_ref.unsubscribe(key)
    return {"status": "unsubscribed", "key": key}

