from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import SessionLocal
from .. import schemas, crud
from ..simulation import run_simulation

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.SimulationResult)
def simulate(req: schemas.SimulationRequest, db: Session = Depends(get_db)):
    # fetch internal constants from DB (will insert defaults if missing)
    consts = crud.get_internal_constants(db)
    result = run_simulation(req, consts)
    return schemas.SimulationResult(**result)


@router.post("/roi", response_model=schemas.SimulationResult)
def simulate_alias(req: schemas.SimulationRequest, db: Session = Depends(get_db)):
    # alias endpoint kept for backward compatibility
    return simulate(req, db)
