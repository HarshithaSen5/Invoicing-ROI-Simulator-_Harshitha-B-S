import React from 'react'
import InvoiceForm from './InvoiceForm'
import './styles.css'

export default function App() {
  return (
    <div className="app-root">
      <header className="app-header">
        <h1>Invoicing ROI Simulator</h1>
        <p className="lead">Quickly model automation ROI, save scenarios, and generate gated reports.</p>
      </header>

      <main className="app-main">
        <section className="left-col">
          <InvoiceForm />
        </section>
        <aside className="right-col">
          <div className="card">
            <h3>How it works</h3>
            <p>Enter your inputs, see instant results, save scenarios, and generate gated reports that require an email before download.</p>
          </div>
        </aside>
      </main>
    </div>
  )
}
