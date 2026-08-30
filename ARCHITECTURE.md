# MVP Architecture

```text
                    ┌──────────────────────┐
                    │      Streamlit UI    │
                    └──────────┬───────────┘
                               │
          ┌────────────────────┼───────────────────┐
          ↓                    ↓                   ↓
     CSV Upload          Product Dashboard     User Actions
          │                    │                   │
          ↓                    ↓                   ↓
     Validation          Metrics / Insights   Session State
          │                    │                   │
          └────────────────────┼───────────────────┘
                               ↓
                      Canonical Transactions
                               │
                 ┌─────────────┴─────────────┐
                 ↓                           ↓
          Categorization                 Planning
          (rule-based)             Budget + Savings Goal
```

## Design decisions

### Streamlit

Chosen for rapid PM prototyping and easy demonstration.

### Rule-based categorization

Chosen because it is:
- transparent
- deterministic
- easy to debug
- appropriate for an MVP prototype

It is not presented as production-grade financial categorization.

### Session state

Used so the prototype can demonstrate interaction without requiring a database.

### Synthetic data

Used to avoid handling real financial information.

## Production evolution

```text
Prototype
  ↓
Secure backend
  ↓
Encrypted storage
  ↓
Authentication
  ↓
Financial-data provider integration
  ↓
Security/compliance review
  ↓
Production launch
```

The production version would require substantially stronger security, privacy, reliability, compliance and data-governance controls.
