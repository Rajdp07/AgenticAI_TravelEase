from fastapi import APIRouter
from app.schemas.models import PredictionRequest, AlternativesRequest, NotifyRequest, AgentRunRequest
from app.services.predictor import PredictorService
from app.services.alternatives import AlternativesService
from app.services.notifier import NotifierService
from app.services.agent import AgentService
from app.routes.monitor import router as monitor_router, init_scheduler

router = APIRouter()

predictor_service = PredictorService()
alternatives_service = AlternativesService()
notifier_service = NotifierService()
agent_service = AgentService(predictor_service, alternatives_service, notifier_service)
init_scheduler(agent_service)

@router.post("/predict")
def predict(req: PredictionRequest):
    return predictor_service.predict(req.flight_info)

@router.post("/alternatives")
def alternatives(req: AlternativesRequest):
    return {"alternatives": alternatives_service.suggest(req.flight_info)}

@router.post("/notify")
def notify(req: NotifyRequest):
    notifier_service.notify(req.message, req.webhook_url)
    return {"status": "sent"}

@router.post("/agent/run")
def agent_run(req: AgentRunRequest):
    return agent_service.run(req.flight_info)

# Mount monitor endpoints
router.include_router(monitor_router)

