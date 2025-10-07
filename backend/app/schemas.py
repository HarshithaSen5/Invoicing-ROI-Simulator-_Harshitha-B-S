from pydantic import BaseModel, Field
from datetime import date
from typing import Optional, Any


class InvoiceCreate(BaseModel):
    customer: str = Field(...)
    description: Optional[str]
    amount: float
    date: date


class InvoiceRead(InvoiceCreate):
    id: int

    class Config:
        orm_mode = True


# Simulation request uses the detailed fields the user provided
class SimulationRequest(BaseModel):
    monthly_invoice_volume: int
    num_ap_staff: int
    avg_hours_per_invoice: float
    hourly_wage: float
    error_rate_manual: float
    error_cost: float
    time_horizon_months: int
    one_time_implementation_cost: float = 0.0


class SimulationResult(BaseModel):
    monthly_savings: float
    cumulative_savings: float
    net_savings: float
    payback_months: float
    roi_percentage: float
    breakdown: Any


class ScenarioCreate(BaseModel):
    scenario_name: str
    monthly_invoice_volume: int
    num_ap_staff: int
    avg_hours_per_invoice: float
    hourly_wage: float
    error_rate_manual: float
    error_cost: float
    time_horizon_months: int
    one_time_implementation_cost: float = 0.0


class ScenarioRead(ScenarioCreate):
    id: int

    class Config:
        orm_mode = True


class ReportRequest(BaseModel):
    scenario_id: Optional[int] = None
    email: str
