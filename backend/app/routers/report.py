from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import SessionLocal
from .. import schemas, crud
import os
import json
from ..simulation import run_simulation
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/generate")
def generate_report(req: schemas.ReportRequest, db: Session = Depends(get_db)):
    # Require email
    if not req.email:
        raise HTTPException(status_code=400, detail="email required")

    # If scenario_id provided, fetch scenario
    scenario = None
    if req.scenario_id:
        scenario = crud.get_scenario(db, req.scenario_id)
        if not scenario:
            raise HTTPException(status_code=404, detail="Scenario not found")

    # Create a simple HTML report snapshot in backend/reports
    reports_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'backend_reports'))
    os.makedirs(reports_dir, exist_ok=True)

    report_data = {
        'email': req.email,
        'scenario': {
            'id': scenario.id if scenario else None,
            'name': scenario.scenario_name if scenario else None,
        }
    }

    report_id = f"report_{req.email.replace('@','_').replace('.','_')}"
    html_path = os.path.join(reports_dir, f"{report_id}.html")
    pdf_path = os.path.join(reports_dir, f"{report_id}.pdf")

    # write html snapshot
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write('<html><body><h1>Invoicing ROI Report</h1>')
        f.write(f"<p>Requested by: {req.email}</p>")
        if scenario:
            f.write(f"<p>Scenario: {scenario.scenario_name}</p>")
        f.write('</body></html>')

    # create PDF using ReportLab
    try:
        c = canvas.Canvas(pdf_path, pagesize=letter)
        width, height = letter
        y = height - 72
        c.setFont('Helvetica-Bold', 16)
        c.drawString(72, y, 'Invoicing ROI Report')
        y -= 30
        c.setFont('Helvetica', 10)
        c.drawString(72, y, f'Requested by: {req.email}')
        y -= 20

        if scenario:
            # if saved scenario exists, include its fields
            c.drawString(72, y, f"Scenario: {scenario.scenario_name}")
            y -= 18
            c.drawString(72, y, f"Monthly invoices: {scenario.monthly_invoice_vol}")
            y -= 14
            c.drawString(72, y, f"AP staff: {scenario.num_ap_staff}")
            y -= 14
            c.drawString(72, y, f"Avg hrs/invoice: {float(scenario.avg_hrs_per_invoice)}")
            y -= 14
            c.drawString(72, y, f"Hourly wage: {float(scenario.hourly_wage)}")
            y -= 18

            # attempt to run simulation for this scenario
            from .. import schemas as _schemas
            simreq = _schemas.SimulationRequest(
                monthly_invoice_volume=int(scenario.monthly_invoice_vol),
                num_ap_staff=int(scenario.num_ap_staff),
                avg_hours_per_invoice=float(scenario.avg_hrs_per_invoice),
                hourly_wage=float(scenario.hourly_wage),
                error_rate_manual=float(scenario.error_rate_manual),
                error_cost=float(scenario.error_cost),
                time_horizon_months=int(scenario.time_horizon_months),
                one_time_implementation_cost=float(scenario.one_time_implementation_cost or 0.0),
            )
            consts = crud.get_internal_constants(db)
            simres = run_simulation(simreq, consts)

            y -= 10
            c.setFont('Helvetica-Bold', 12)
            c.drawString(72, y, 'Simulation Results')
            y -= 18
            c.setFont('Helvetica', 10)
            c.drawString(72, y, f"Monthly savings: {simres['monthly_savings']:.2f}")
            y -= 14
            c.drawString(72, y, f"Cumulative savings: {simres['cumulative_savings']:.2f}")
            y -= 14
            c.drawString(72, y, f"Payback months: {simres['payback_months']:.2f}")
            y -= 14
            c.drawString(72, y, f"ROI %: {simres['roi_percentage']:.2f}")
            y -= 14

        c.showPage()
        c.save()
    except Exception as e:
        # on failure to create PDF, return html only
        return {"html_url": f"/backend_reports/{os.path.basename(html_path)}", "error": str(e)}

    return {"html_url": f"/backend_reports/{os.path.basename(html_path)}", "pdf_url": f"/backend_reports/{os.path.basename(pdf_path)}"}
