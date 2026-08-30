# MoneyFlow — Personal Finance Product Strategy & Launch

> **Pure Product Management Case Study | FinTech | Discovery → Strategy → MVP → PRD → Roadmap → GTM → Metrics**

**MoneyFlow** is a product-management case study for a privacy-conscious personal finance companion designed for students and early-career professionals who struggle to turn transaction data into clear, actionable financial decisions.

This repository is intentionally **PM-first**. It does not present a finance app as a finished software project. Instead, it documents how a Product Manager would identify a problem, validate it, define an MVP, prioritize the roadmap, design the experience, establish metrics, prepare a launch, and learn after release.

---

**FinTech Product Management case study + working MVP for a privacy-first personal finance decision-support product.**

[![🚀 Live MVP](https://img.shields.io/badge/🚀%20Live%20MVP-Open%20MoneyFlow-0f766e?style=for-the-badge&logo=streamlit&logoColor=white)](https://moneyflow-appuct-management-abhi-iitg.streamlit.app/)
[![GitHub](https://img.shields.io/badge/GitHub-Source%20Code-181717?style=for-the-badge&logo=github)](https://github.com/abhi-iitg/moneyflow-product-management)

### Live Product

**[Open the MoneyFlow Working MVP →](https://moneyflow-appuct-management-abhi-iitg.streamlit.app/)**

> **Demo:** The MVP uses synthetic/demo financial data. Never upload bank passwords, OTPs, card numbers, account credentials, or other sensitive information.

---

## Executive Summary

### The problem

Young adults can see transactions in banking apps, but transaction visibility does not automatically create financial control. Users commonly face three connected problems:

1. **Understanding:** "Where did my money go?"
2. **Planning:** "Can I safely spend this month?"
3. **Action:** "What should I do differently before I run out of money?"

Existing solutions often overload users with charts, categories, or generic budgeting advice. MoneyFlow proposes a simpler loop:

**See → Understand → Plan → Act → Learn**

### Target user

**Primary persona:** students and early-career professionals with irregular discretionary spending, multiple recurring payments, and limited time for manual financial planning.

### Product promise

> **MoneyFlow turns transaction history into a small number of clear, explainable actions.**

### MVP

The MVP focuses on four capabilities:

- privacy-first transaction import
- automatic spending categorization with user correction
- monthly cash-flow and spending view
- actionable budget and savings prompts

The MVP deliberately excludes investing advice, lending, payments, credit decisions, tax advice, and autonomous financial actions.

## 📸 MVP Screenshots

### MoneyFlow — Financial Check-in Dashboard

![MoneyFlow Financial Check-in Dashboard](docs/screenshots/moneyflow-dashboard.png)

### 2. Transaction Management

![MoneyFlow Transactions](docs/screenshots/moneyflow-transactions.png)

### 3. Budget Planning

![MoneyFlow Planning](docs/screenshots/moneyflow-planning.png)

### 4. Product Metrics

![MoneyFlow Product Metrics](docs/screenshots/moneyflow-product-metrics.png)

### 🚀 Live Demo

**[Open MoneyFlow MVP →](https://moneyflow-appuct-management-abhi-iitg.streamlit.app/)**

*Working MVP using synthetic/demo transaction data.*

### What the MVP demonstrates

- 💰 Income and expense overview
- 📈 Net cash-flow visibility
- 🔎 "What changed?" actionable insights
- 📊 Spending-by-category analysis
- 📁 CSV transaction upload
- ✏️ Transaction categorization and correction
- 🎯 Budget and savings-goal planning
- 🔐 Privacy-first data handling

### North Star Metric

**Weekly Actionable Financial Check-ins (WAFC)**

A check-in counts when a user views their current financial status **and completes at least one meaningful action**, such as correcting a category, setting/adjusting a budget, acknowledging a recurring expense, or updating a savings goal.

This metric is chosen because MoneyFlow's value proposition is not "more dashboard views"; it is helping users understand and act.

### Target outcomes for MVP

These are **product targets, not measured results**:

- ≥ 45% of activated users complete one actionable check-in in their first 7 days
- ≥ 35% of activated users return for a second weekly check-in by week 4
- ≥ 60% of imported transactions are correctly categorized without manual correction after the first two weeks
- < 2% of imported rows fail validation
- < 1% of users report a high-severity privacy/trust issue

---

## Product Decision in One Page

| Question | Decision |
|---|---|
| Who? | Students + early-career professionals |
| Problem? | Transaction visibility does not translate into financial action |
| Wedge? | Actionable monthly cash-flow clarity |
| MVP? | Import → categorize → understand → plan |
| Primary value metric? | Weekly Actionable Financial Check-ins |
| Business model? | Free core + optional premium planning features |
| Primary growth loop? | Personal value → recurring check-in → referral |
| Biggest risk? | Trust/privacy failure |
| Biggest product bet? | Fewer, explainable actions beat dashboard overload |
| What we will NOT do? | Investment, lending, tax, payments, autonomous money movement |

---

## Repository Map

```text
MoneyFlow-Product-Management/
├── README.md
├── LICENSE
├── .gitignore
├── 01-discovery/
│   ├── problem-statement.md
│   ├── user-research-plan.md
│   ├── personas.md
│   ├── JTBD.md
│   ├── customer-journey.md
│   └── opportunity-solution-tree.md
├── 02-market/
│   ├── competitive-analysis.md
│   ├── market-sizing.md
│   └── positioning.md
├── 03-strategy/
│   ├── product-vision.md
│   ├── product-strategy.md
│   ├── business-model.md
│   └── product-principles.md
├── 04-prioritization/
│   ├── feature-backlog.md
│   ├── RICE-prioritization.md
│   └── MVP-scope.md
├── 05-prd/
│   ├── PRD.md
│   ├── user-stories.md
│   ├── acceptance-criteria.md
│   └── non-functional-requirements.md
├── 06-ux/
│   ├── information-architecture.md
│   ├── user-flows.md
│   └── wireframe-spec.md
├── 07-roadmap/
│   ├── product-roadmap.md
│   └── release-plan.md
├── 08-metrics/
│   ├── north-star-metric.md
│   ├── metrics-tree.md
│   ├── funnel.md
│   └── KPI-dictionary.md
├── 09-launch/
│   ├── GTM-strategy.md
│   ├── launch-plan.md
│   └── stakeholder-plan.md
├── 10-experimentation/
│   ├── experiment-backlog.md
│   └── experiment-01-onboarding.md
├── 11-risk/
│   ├── risk-register.md
│   ├── privacy-trust.md
│   └── assumptions.md
├── 12-post-launch/
│   ├── 30-60-90-day-plan.md
│   └── iteration-framework.md
└── portfolio/
    └── case-study.md
```

---

## Product Method

MoneyFlow follows a repeatable PM operating loop:

**Discover**
→ identify the highest-value user problem

**Define**
→ establish target user, JTBD, opportunity and constraints

**Strategize**
→ choose a differentiated wedge and business model

**Prioritize**
→ compare opportunities using RICE + strategic fit

**Specify**
→ write the PRD, stories and acceptance criteria

**Design**
→ map information architecture and critical user flows

**Plan**
→ sequence releases around outcomes, not feature volume

**Launch**
→ coordinate GTM, instrumentation, support and risk controls

**Learn**
→ evaluate metrics and experiments, then iterate

---

## Evidence Discipline

This case study separates:

- **Evidence:** findings supported by cited research or clearly stated assumptions
- **Hypothesis:** a belief to validate
- **Target:** an intended future outcome
- **Decision:** a deliberate product choice
- **Result:** a measured outcome after launch

No fictional survey result, customer quote, revenue number, conversion result, or A/B-test outcome is presented as if it actually happened.

---

## Research Basis

The product structure was informed by public GitHub PM/FinTech references including:

- personal-finance PRD patterns
- FinTech product analytics and lifecycle analysis
- SMB financial workflow products
- FinTech competitive/product case studies
- PM frameworks for PRDs, MVPs, prioritization and roadmaps

The repository is an **original case study**. No source repository is copied, forked, or represented as MoneyFlow.

---

## Important Disclaimer

MoneyFlow is a product-management case study and not a regulated financial service. It does not provide investment, tax, legal, lending, credit, accounting, or financial advice. Any financial examples are illustrative.

---

## Portfolio Positioning

**Resume project title:**

> **MoneyFlow — Personal Finance Product Strategy & Launch**

**One-line description:**

> Designed a privacy-first personal finance product from discovery to launch, defining the MVP, PRD, RICE roadmap, UX flows, KPI tree, GTM strategy and experimentation plan for students and early-career professionals.

---


## Working MVP

This repository now includes a runnable Streamlit prototype that demonstrates the core product loop:

**Import → Validate → Categorize → Understand → Plan → Act → Measure**

### Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

See **[RUN_MVP.md](RUN_MVP.md)** for the complete test procedure and **[DEMO_SCRIPT.md](DEMO_SCRIPT.md)** for a recruiter demo walkthrough.

The prototype uses synthetic data, transparent rule-based categorization, session state, CSV import, category correction, budgets, savings goals, actionable insights and session-level product instrumentation.

## Author

**Abhishek Kumar Gond**  
IIT Guwahati | Product Management / Data & AI
- **Email : mr.abhishekaaa@gmail.com**
- **[Portfolio]()**
- **[LinkedIn](https://www.linkedin.com/in/abhishekkumargond/)**

## License

Released under the [MIT License](LICENSE).
