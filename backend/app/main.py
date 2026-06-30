from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from app import models  # noqa: F401 - ensures models are registered on Base before create_all
from app.database import Base, engine
from app.routes import (
    calendar_routes,
    category_routes,
    dashboard_routes,
    installment_purchase_routes,
    recurring_expense_routes,
    report_routes,
    user_routes,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="ParcelaFácil API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_routes.router)
app.include_router(category_routes.router)
app.include_router(recurring_expense_routes.router)
app.include_router(installment_purchase_routes.router)
app.include_router(dashboard_routes.router)
app.include_router(calendar_routes.router)
app.include_router(report_routes.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/")
def root():
    return RedirectResponse(url="/pages/dashboard.html")


FRONTEND_DIR = Path(__file__).resolve().parent.parent.parent / "frontend"
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
