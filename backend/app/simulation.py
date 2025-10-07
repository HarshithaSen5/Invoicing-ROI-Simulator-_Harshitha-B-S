from . import schemas


def run_simulation(req: schemas.SimulationRequest, consts):
    # translate fields
    monthly_invoice_volume = req.monthly_invoice_volume
    num_ap_staff = req.num_ap_staff
    avg_hours = req.avg_hours_per_invoice
    hourly_wage = req.hourly_wage
    # Inputs are expected as percentages (e.g. 0.5 means 0.5%)
    error_rate_manual = float(req.error_rate_manual) / 100.0
    error_cost = req.error_cost
    time_horizon = req.time_horizon_months
    one_time = req.one_time_implementation_cost

    # internal constants from DB model (SQLAlchemy row)
    automated_cost_per_invoice = float(consts.automated_cost_per_invoice)
    # internal constant stored as percentage (e.g. 0.1 for 0.1%)
    error_rate_auto = float(consts.error_rate_auto) / 100.0
    time_saved_per_invoice = float(consts.time_saved_per_invoice) / 60.0  # convert minutes to hours
    min_roi_boost_factor = float(consts.min_roi_boost_factor)

    # 1. manual labor cost per month
    labor_cost_manual = num_ap_staff * hourly_wage * avg_hours * monthly_invoice_volume

    # 2. automation cost per month
    auto_cost = monthly_invoice_volume * automated_cost_per_invoice

    # 3. error savings
    error_savings = (error_rate_manual - error_rate_auto) * monthly_invoice_volume * error_cost

    # baseline monthly savings
    monthly_savings = (labor_cost_manual + error_savings) - auto_cost

    # apply bias to ensure favorable output
    monthly_savings = monthly_savings * min_roi_boost_factor

    # cumulative and ROI
    cumulative_savings = monthly_savings * time_horizon
    net_savings = cumulative_savings - one_time

    payback_months = None
    if monthly_savings > 0:
        payback_months = one_time / monthly_savings
    else:
        payback_months = float('inf')

    roi_percentage = 0.0
    if one_time > 0:
        roi_percentage = (net_savings / one_time) * 100.0

    breakdown = {
        'labor_cost_manual': labor_cost_manual,
        'auto_cost': auto_cost,
        'error_savings': error_savings,
        'min_roi_boost_factor': min_roi_boost_factor,
    }

    return {
        'monthly_savings': monthly_savings,
        'cumulative_savings': cumulative_savings,
        'net_savings': net_savings,
        'payback_months': payback_months,
        'roi_percentage': roi_percentage,
        'breakdown': breakdown,
    }
