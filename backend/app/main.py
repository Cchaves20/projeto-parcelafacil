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
    savings_box_routes,
    sporadic_expense_routes,
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
app.include_router(sporadic_expense_routes.router)
app.include_router(savings_box_routes.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/")
def root():
    return RedirectResponse(url="/pages/dashboard.html")


_base = Path(__file__).resolve().parent.parent
_candidates = [
    _base / "frontend_dist",          # Dockerfile or nixpacks (cd backend)
    Path("/app/frontend_dist"),        # Dockerfile absolute
    Path("/app/backend/frontend_dist"), # nixpacks absolute
    _base.parent / "frontend",         # local dev
    Path("/frontend"),                 # nixpacks alternate
]
FRONTEND_DIR = next((p for p in _candidates if p.exists()), None)
if FRONTEND_DIR is None:
    raise RuntimeError(f"Frontend directory not found. Tried: {[str(p) for p in _candidates]}")
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
