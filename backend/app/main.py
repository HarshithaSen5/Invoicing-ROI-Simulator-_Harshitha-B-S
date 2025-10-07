from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from .db import engine, Base
from .routers import invoices, simulate, scenarios, report

app = FastAPI(title="Invoicing ROI Simulator")

# CORS - allow the frontend dev server and localhost
origins = [
	"http://localhost",
	"http://localhost:3000",
	"http://127.0.0.1",
	"http://127.0.0.1:3000",
]

app.add_middleware(
	CORSMiddleware,
	allow_origins=origins,
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

# Serve generated reports (HTML/PDF) from backend_reports folder
reports_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend_reports'))
os.makedirs(reports_path, exist_ok=True)
app.mount("/backend_reports", StaticFiles(directory=reports_path), name="backend_reports")

Base.metadata.create_all(bind=engine)

app.include_router(invoices.router, prefix="/invoices", tags=["invoices"])
app.include_router(simulate.router, prefix="/simulate", tags=["simulate"])
app.include_router(scenarios.router, prefix="/scenarios", tags=["scenarios"])
app.include_router(report.router, prefix="/report", tags=["report"])
