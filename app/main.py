from fastapi import FastAPI
from app.routes import routes

app = FastAPI(title="Flight Disruption AI Agent")

app.include_router(routes.router)

@app.get("/health")
def health():
    return {"status": "ok"}

