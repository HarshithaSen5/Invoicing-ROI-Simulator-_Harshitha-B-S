from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from .db import Base


class Invoice(Base):
    __tablename__ = 'invoices'

    id = Column(Integer, primary_key=True, index=True)
    customer = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    amount = Column(Numeric(12, 2), nullable=False)
    date = Column(Date, nullable=False)



class UserInput(Base):
    __tablename__ = 'user_input'

    id = Column(Integer, primary_key=True, index=True)
    scenario_name = Column(String(255), nullable=False)
    monthly_invoice_vol = Column(Integer)
    num_ap_staff = Column(Integer)
    avg_hrs_per_invoice = Column(Numeric(12,4))
    hourly_wage = Column(Numeric(12,2))
    error_rate_manual = Column(Numeric(10,4))
    error_cost = Column(Numeric(12,2))
    time_horizon_months = Column(Integer)
    one_time_implementation_cost = Column(Numeric(12,2))


class InternalConstants(Base):
    __tablename__ = 'internal_constants'

    id = Column(Integer, primary_key=True)
    automated_cost_per_invoice = Column(Numeric(12,4), nullable=False)
    error_rate_auto = Column(Numeric(10,4), nullable=False)
    time_saved_per_invoice = Column(Integer, nullable=False)
    min_roi_boost_factor = Column(Numeric(10,4), nullable=False)


class Scenario(Base):
    __tablename__ = 'scenarios'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    owner_email = Column(String(255), nullable=True)
    # store JSON payload as text
    payload = Column(Text, nullable=False)
    result = Column(Text, nullable=True)

