# Wholesale Fashion Retailer — Financial Health Analysis

Financial analysis of a wholesale/retail apparel business, built from real accounting
ledgers (creditor/supplier ledger, debtor/customer ledger, and trading P&L account),
anonymized for public sharing.

> **On the data:** this project is based on a real small business's FY financial
> records. Company name, client names, and supplier names have been replaced with
> generic labels, and all figures have been randomly adjusted (±6%) so exact real
> numbers cannot be reconstructed — while preserving the same overall financial
> story and ratios. The analysis code runs unchanged against real ledger exports
> with the same column structure.

## What this analyzes

- **P&L waterfall** — how sales flow down to gross profit/loss and net profit/loss
- **Operating expense breakdown** — largest fixed costs (salaries, rent, etc.)
- **Supplier concentration** — how purchase volume is distributed across suppliers
- **Customer concentration** — how sales are distributed across customers
- **Receivables vs. payables** — outstanding balances at period end, and which
  relationships dominate each side

## Project structure

```
.
├── analysis.py               # cleans data, runs analysis, generates charts + insights.md
├── data/
│   ├── suppliers.csv         # per-supplier purchases, payments, balance
│   ├── customers.csv          # per-customer sales, payments received, balance
│   └── pnl.csv                 # full P&L line items
├── charts/                     # generated PNG charts
└── insights.md                  # written summary of findings
```

## How to run

```bash
pip install pandas numpy matplotlib
python3 analysis.py        # runs the analysis, writes charts/ and insights.md
```

To run on a different business's real data, replace the three CSVs in `data/`
with exports using the same column names.

## Sample findings

See [`insights.md`](insights.md) for the full write-up. Headline findings:

- The business closed the year with a **net loss** — direct purchase and production
  costs alone exceeded total sales, before any operating expenses were counted.
- **Salaries and rent** are the two largest fixed operating costs, together consuming
  a substantial share of revenue regardless of monthly sales performance.
- A **single supplier accounts for roughly three-quarters of all purchase volume**,
  representing significant supply-chain concentration risk.
- **Sales are similarly concentrated** in a small number of large wholesale accounts
  rather than spread across many customers.
- Ledger-tracked customer sales are lower than the total P&L sales figure, suggesting
  some revenue (e.g. daily till/livestream sales) is recorded in aggregate rather
  than per customer — a data-completeness gap worth investigating further.

## Why this project

Real small businesses rarely have clean, analysis-ready data — this project works
directly from raw accounting ledger exports (the kind produced by standard SME
bookkeeping software), demonstrating data cleaning, aggregation, and building a
narrative from messy real-world financial records rather than a pre-cleaned dataset.

## Tools used

Python, pandas, numpy, matplotlib.

---
*Author: Syed Altamash Ali*
