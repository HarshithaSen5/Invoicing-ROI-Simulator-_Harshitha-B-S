import React, { useState, useEffect } from 'react'
import axios from 'axios'

export default function InvoiceForm(){
  // Scenario inputs
  const [scenario_name, setScenarioName] = useState('')
  const [monthly_invoice_volume, setMonthlyInvoiceVolume] = useState(2000)
  const [num_ap_staff, setNumApStaff] = useState(3)
  const [avg_hours_per_invoice, setAvgHoursPerInvoice] = useState(0.1667)
  const [hourly_wage, setHourlyWage] = useState(30)
  const [error_rate_manual, setErrorRateManual] = useState(0.5)
  const [error_cost, setErrorCost] = useState(100)
  const [time_horizon_months, setTimeHorizonMonths] = useState(36)
  const [one_time_implementation_cost, setOneTime] = useState(50000)

  const [simResult, setSimResult] = useState(null)
  const [status, setStatus] = useState(null)
  const [scenarios, setScenarios] = useState([])
  const [emailForReport, setEmailForReport] = useState('')
  const [selectedScenarioId, setSelectedScenarioId] = useState(null)

  const payload = () => ({
    monthly_invoice_volume: Number(monthly_invoice_volume),
    num_ap_staff: Number(num_ap_staff),
    avg_hours_per_invoice: Number(avg_hours_per_invoice),
    hourly_wage: Number(hourly_wage),
    error_rate_manual: Number(error_rate_manual),
    error_cost: Number(error_cost),
    time_horizon_months: Number(time_horizon_months),
    one_time_implementation_cost: Number(one_time_implementation_cost),
  })

  async function runSimulation(e){
    if(e) e.preventDefault()
    try{
      const res = await axios.post('http://127.0.0.1:8000/simulate/', payload())
      setSimResult(res.data)
    }catch(err){
      console.error(err)
      setStatus('Error running simulation')
      setTimeout(()=>setStatus(null),2500)
    }
  }

  async function saveScenario(e){
    if(e) e.preventDefault()
    if(!scenario_name) return setStatus('Enter scenario name')
    try{
      await axios.post('http://127.0.0.1:8000/scenarios/', { scenario_name, ...payload() })
      setStatus('Scenario saved')
      setTimeout(()=>setStatus(null),2500)
      loadScenarios()
    }catch(err){
      console.error(err)
      setStatus('Error saving scenario')
    }
  }

  async function loadScenarios(){
    try{
      const res = await axios.get('http://127.0.0.1:8000/scenarios/')
      setScenarios(res.data)
    }catch(e){
      console.error('loadScenarios', e)
    }
  }

  useEffect(()=>{ loadScenarios() }, [])

  async function loadScenario(id){
    try{
      const res = await axios.get(`http://127.0.0.1:8000/scenarios/${id}`)
      const p = res.data
      setMonthlyInvoiceVolume(p.monthly_invoice_volume)
      setNumApStaff(p.num_ap_staff)
      setAvgHoursPerInvoice(p.avg_hours_per_invoice)
      setHourlyWage(p.hourly_wage)
      setErrorRateManual(p.error_rate_manual)
      setErrorCost(p.error_cost)
      setTimeHorizonMonths(p.time_horizon_months)
      setOneTime(p.one_time_implementation_cost)
      setScenarioName(p.scenario_name)
      // run simulation after loading
      const res2 = await axios.post('http://127.0.0.1:8000/simulate/', payload())
      setSimResult(res2.data)
    }catch(e){
      console.error('loadScenario', e)
    }
  }

  async function deleteScenario(id){
    try{
      await axios.delete(`http://127.0.0.1:8000/scenarios/${id}`)
      loadScenarios()
    }catch(e){ console.error(e) }
  }

  async function generateReport(){
    if(!emailForReport) return alert('Enter email to generate report')
    try{
      const res = await axios.post('http://127.0.0.1:8000/report/generate', { email: emailForReport, scenario_id: selectedScenarioId })
      const msg = []
      if(res.data.pdf_url){
        const pdfUrl = res.data.pdf_url
        // open in new tab (browser will download or view PDF)
        window.open(pdfUrl, '_blank')
      }
      if(res.data.html_url){
        const htmlUrl = res.data.html_url
        // open html snapshot as well
        window.open(htmlUrl, '_blank')
      }
    }catch(e){ console.error('generateReport', e) }
  }

  // Keep minimal invoice creation below (optional)
  const [customer, setCustomer] = useState('')
  const [amount, setAmount] = useState('')
  const [date, setDate] = useState(new Date().toISOString().slice(0,10))

  async function createInvoice(e){
    e.preventDefault()
    try{
      await axios.post('http://127.0.0.1:8000/invoices/', { customer, amount: Number(amount), date })
      setCustomer(''); setAmount('')
      setStatus('Invoice created')
      setTimeout(()=>setStatus(null),2000)
    }catch(err){
      setStatus('Invoice error')
    }
  }

  return (
    <div className="card">
      <h2>Scenario Inputs</h2>
      <form onSubmit={runSimulation}>
        <div className="grid">
          <div>
            <label>Scenario name</label>
            <input value={scenario_name} onChange={e=>setScenarioName(e.target.value)} placeholder='Q4_Pilot' />
          </div>
          <div>
            <label>Monthly invoice volume</label>
            <input type='number' value={monthly_invoice_volume} onChange={e=>setMonthlyInvoiceVolume(e.target.value)} />
          </div>
          <div>
            <label>AP staff</label>
            <input type='number' value={num_ap_staff} onChange={e=>setNumApStaff(e.target.value)} />
          </div>
          <div>
            <label>Avg hours per invoice</label>
            <input type='number' step='0.01' value={avg_hours_per_invoice} onChange={e=>setAvgHoursPerInvoice(e.target.value)} />
          </div>
          <div>
            <label>Hourly wage</label>
            <input type='number' value={hourly_wage} onChange={e=>setHourlyWage(e.target.value)} />
          </div>
          <div>
            <label>Error rate manual (%)</label>
            <input type='number' step='0.01' value={error_rate_manual} onChange={e=>setErrorRateManual(e.target.value)} />
          </div>
          <div>
            <label>Error cost</label>
            <input type='number' value={error_cost} onChange={e=>setErrorCost(e.target.value)} />
          </div>
          <div>
            <label>Time horizon months</label>
            <input type='number' value={time_horizon_months} onChange={e=>setTimeHorizonMonths(e.target.value)} />
          </div>
          <div>
            <label>One-time implementation cost</label>
            <input type='number' value={one_time_implementation_cost} onChange={e=>setOneTime(e.target.value)} />
          </div>
        </div>

        <div className="controls" style={{marginTop:8}}>
          <button className='btn' type='submit'>Run Simulation</button>
          <button className='btn' style={{background:'#10b981'}} onClick={saveScenario}>Save Scenario</button>
          {status && <div className='small muted'>{status}</div>}
        </div>
      </form>

      {simResult && (
        <div className='result-card'>
          <div><strong>Monthly savings:</strong> ${simResult.monthly_savings.toFixed(2)}</div>
          <div><strong>Cumulative ({time_horizon_months}m):</strong> ${simResult.cumulative_savings.toFixed(2)}</div>
          <div><strong>Payback:</strong> {isFinite(simResult.payback_months) ? simResult.payback_months.toFixed(1) + ' months' : 'N/A'}</div>
          <div><strong>ROI %:</strong> {simResult.roi_percentage.toFixed(1)}%</div>
        </div>
      )}

      <hr style={{margin:'12px 0'}} />

      <h3>Create Invoice (optional)</h3>
      <form onSubmit={createInvoice}>
        <div className='grid'>
          <div>
            <label>Customer</label>
            <input value={customer} onChange={e=>setCustomer(e.target.value)} />
          </div>
          <div>
            <label>Amount</label>
            <input type='number' value={amount} onChange={e=>setAmount(e.target.value)} />
          </div>
        </div>
        <div style={{marginTop:8}}>
          <button className='btn' type='submit'>Create Invoice</button>
        </div>
      </form>

      <div style={{marginTop:12}}>
        <h3>Generate gated report</h3>
        <div style={{display:'grid',gridTemplateColumns:'1fr 160px',gap:8}}>
          <div>
            <label>Email for report</label>
            <input placeholder='lead@example.com' value={emailForReport} onChange={e=>setEmailForReport(e.target.value)} />
          </div>
          <div>
            <label>Saved scenario</label>
            <select value={selectedScenarioId || ''} onChange={e=>setSelectedScenarioId(e.target.value || null)}>
              <option value=''>(none)</option>
              {scenarios.map(s=> (<option key={s.id} value={s.id}>{s.scenario_name}</option>))}
            </select>
          </div>
        </div>
        <div style={{marginTop:8}}>
          <button className='btn' onClick={generateReport}>Generate & Download PDF</button>
        </div>
      </div>
    </div>
  )
}
