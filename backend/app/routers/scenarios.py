from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import SessionLocal
from .. import schemas, crud

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.ScenarioRead)
def create_scenario(sc: schemas.ScenarioCreate, db: Session = Depends(get_db)):
    return crud.create_user_input(db, sc)


@router.get("/", response_model=list[schemas.ScenarioRead])
def list_scenarios(db: Session = Depends(get_db)):
    rows = crud.list_user_inputs(db)
    # convert DB model to ScenarioRead-like dict
    out = []
    for r in rows:
        out.append({
            'id': r.id,
            'scenario_name': r.scenario_name,
            'monthly_invoice_volume': r.monthly_invoice_vol,
            'num_ap_staff': r.num_ap_staff,
            'avg_hours_per_invoice': float(r.avg_hrs_per_invoice),
            'hourly_wage': float(r.hourly_wage),
            'error_rate_manual': float(r.error_rate_manual),
            'error_cost': float(r.error_cost),
            'time_horizon_months': r.time_horizon_months,
            'one_time_implementation_cost': float(r.one_time_implementation_cost),
        })
    return out


@router.get("/{scenario_id}", response_model=schemas.ScenarioRead)
def get_scenario(scenario_id: int, db: Session = Depends(get_db)):
    s = crud.get_user_input(db, scenario_id)
    if not s:
        raise HTTPException(status_code=404, detail="Scenario not found")
    return {
        'id': s.id,
        'scenario_name': s.scenario_name,
        'monthly_invoice_volume': s.monthly_invoice_vol,
        'num_ap_staff': s.num_ap_staff,
        'avg_hours_per_invoice': float(s.avg_hrs_per_invoice),
        'hourly_wage': float(s.hourly_wage),
        'error_rate_manual': float(s.error_rate_manual),
        'error_cost': float(s.error_cost),
        'time_horizon_months': s.time_horizon_months,
        'one_time_implementation_cost': float(s.one_time_implementation_cost),
    }


@router.delete("/{scenario_id}")
def delete_scenario(scenario_id: int, db: Session = Depends(get_db)):
    s = crud.delete_user_input(db, scenario_id)
    if not s:
        raise HTTPException(status_code=404, detail="Scenario not found")
    return {"deleted": True}
