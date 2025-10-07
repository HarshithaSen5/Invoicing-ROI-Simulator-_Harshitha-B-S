# Invoicing ROI Simulator

This repository contains a minimal starter for an Invoicing ROI Simulator:
- Backend: FastAPI (Python) + SQLAlchemy + MySQL
- Frontend: React (basic scaffold) + Axios

What you get:
- A FastAPI app exposing invoice CRUD and an ROI simulation endpoint
- SQL schema and example seed file for MySQL
- A minimal React frontend that can post invoices and run simulation

Quick setup (Windows PowerShell):

1) Backend

Create a virtualenv, install dependencies and run the API:

```powershell
cd .\backend
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
# copy and edit .env.example to .env with your MySQL settings
python run.py
```

Default API will run at http://127.0.0.1:8000

2) Database

Run the SQL in `backend/seed.sql` on your MySQL server (or use MySQL Workbench / CLI)

3) Frontend

Use CRA or run the minimal react app:

```powershell
cd .\frontend
npm install
npm start
```

Notes:
- This is a starter scaffold. You should secure the .env values and productionize the setup (migrations, tests, input validation, auth) before using in production.
