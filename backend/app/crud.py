from sqlalchemy.orm import Session
from . import models, schemas
from datetime import date
import json


def create_invoice(db: Session, invoice: schemas.InvoiceCreate):
    db_invoice = models.Invoice(
        customer=invoice.customer,
        description=invoice.description,
        amount=invoice.amount,
        date=invoice.date,
    )
    db.add(db_invoice)
    db.commit()
    db.refresh(db_invoice)
    return db_invoice


def list_invoices(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Invoice).offset(skip).limit(limit).all()


def get_invoice(db: Session, invoice_id: int):
    return db.query(models.Invoice).filter(models.Invoice.id == invoice_id).first()


def create_user_input(db: Session, sc: schemas.ScenarioCreate):
    obj = models.UserInput(
        scenario_name=sc.scenario_name,
        monthly_invoice_vol=sc.monthly_invoice_volume,
        num_ap_staff=sc.num_ap_staff,
        avg_hrs_per_invoice=sc.avg_hours_per_invoice,
        hourly_wage=sc.hourly_wage,
        error_rate_manual=sc.error_rate_manual,
        error_cost=sc.error_cost,
        time_horizon_months=sc.time_horizon_months,
        one_time_implementation_cost=sc.one_time_implementation_cost,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def list_user_inputs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.UserInput).offset(skip).limit(limit).all()


def get_user_input(db: Session, scenario_id: int):
    return db.query(models.UserInput).filter(models.UserInput.id == scenario_id).first()


def delete_user_input(db: Session, scenario_id: int):
    obj = get_user_input(db, scenario_id)
    if obj:
        db.delete(obj)
        db.commit()
    return obj


def get_internal_constants(db: Session):
    # return the first row or defaults if missing
    row = db.query(models.InternalConstants).first()
    if not row:
        # sensible defaults matching user's internal constants
        row = models.InternalConstants(
            automated_cost_per_invoice=0.20,
            error_rate_auto=0.1, # 0.1% (stored as percent)
            time_saved_per_invoice=8,
            min_roi_boost_factor=1.1,
        )
        db.add(row)
        db.commit()
        db.refresh(row)
    return row


def create_scenario(db: Session, name: str, payload: dict, owner_email: str | None = None, result: dict | None = None):
    db_s = models.Scenario(name=name, payload=json.dumps(payload), owner_email=owner_email, result=(json.dumps(result) if result else None))
    db.add(db_s)
    db.commit()
    db.refresh(db_s)
    return db_s


def list_scenarios(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Scenario).offset(skip).limit(limit).all()


def get_scenario(db: Session, scenario_id: int):
    return db.query(models.Scenario).filter(models.Scenario.id == scenario_id).first()


def delete_scenario(db: Session, scenario_id: int):
    s = get_scenario(db, scenario_id)
    if s:
        db.delete(s)
        db.commit()
    return s
