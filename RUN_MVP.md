# MoneyFlow — Run the Working MVP

## 1. Install Python

Use Python 3.10+.

Check:

```bash
python --version
```

## 2. Open the project folder

```bash
cd MoneyFlow-Product-Management
```

## 3. Create a virtual environment

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 4. Install dependencies

```bash
pip install -r requirements.txt
```

## 5. Start MoneyFlow

```bash
streamlit run app.py
```

A browser window should open automatically. If it does not, Streamlit prints a local URL in the terminal.

## 6. Test the core product loop

### Test A — Demo data

1. Open the app.
2. Confirm Income, Expenses and Net Cash Flow appear.
3. Review "What changed?"
4. Click an insight action.
5. Open **Product Metrics**.
6. Confirm "Actions completed" increments.

### Test B — CSV import

1. Open `sample_data/moneyflow_demo.csv`.
2. Upload it from the sidebar.
3. Confirm the dashboard recalculates.
4. Search for `Uber` in Transactions.
5. Open Plan.
6. Change a budget.
7. Open Goal.
8. Change the savings target.

### Test C — Category correction

1. Upload the demo CSV.
2. Go to Transactions.
3. Change a category using the dropdown.
4. Click **Save category corrections**.
5. Confirm the category persists after the page refresh.

### Test D — Bad CSV

Create a CSV missing `amount`:

```csv
date,merchant
2026-08-01,Example
```

Upload it.

Expected behavior:
- the app does not crash
- a clear missing-column error is shown

## 7. What "working" means

This MVP demonstrates the PM case-study's core value loop:

```text
Import
  ↓
Validate
  ↓
Categorize
  ↓
Understand
  ↓
Plan
  ↓
Act
  ↓
Measure
```

It intentionally uses synthetic/demo data and a transparent rule-based categorizer.

## 8. Important safety boundary

Do not upload:
- bank passwords
- OTPs
- card numbers
- account numbers
- private financial exports you are not authorized to process

This is a portfolio prototype, not a regulated financial service.

## 9. Optional deployment

After local testing, deploy the public demo using a platform that supports Streamlit applications. Keep secrets and real financial data out of the repository.
