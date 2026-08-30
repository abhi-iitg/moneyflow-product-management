# Product Requirements Document

## 1. Overview

**Product:** MoneyFlow  
**Release:** MVP v1  
**Owner:** Product Manager  
**Primary users:** Students and early-career professionals

## 2. Problem

Users have transaction data but struggle to convert it into a clear understanding of current spending and a practical next action.

## 3. Goal

Create a low-maintenance weekly financial check-in that helps users understand cash flow and take one meaningful planning action.

## 4. Non-goals

- investment recommendations
- lending
- tax preparation
- payment execution
- credit scoring
- autonomous financial decisions

## 5. User experience

### Entry

User sees:
- current month status
- key change since last check-in
- next action

### Detail

User can:
- inspect transactions
- correct categories
- review recurring commitments
- adjust budget
- update savings goal

### Exit

User completes a meaningful action and receives confirmation.

## 6. Functional requirements

### FR-01 Import
System shall accept a supported CSV format and preview records before saving.

### FR-02 Validation
System shall identify missing dates, invalid amounts and malformed rows before analysis.

### FR-03 Categorization
System shall assign a category using deterministic rules and permit user correction.

### FR-04 Cash-flow
System shall display income, expenses, net cash flow and discretionary spending.

### FR-05 Recurring expenses
System shall flag probable recurring expenses with an explanation of the rule used.

### FR-06 Budget
User shall create and edit flexible category budgets.

### FR-07 Savings goal
User shall create one goal with target amount and target date.

### FR-08 Check-in
System shall generate a weekly summary containing no more than three priority insights.

### FR-09 Action
Each priority insight shall have at least one available action.

### FR-10 Privacy
User shall be able to view, export and delete imported data.

## 7. Product logic

The product should avoid prescriptive financial advice.

Instead of:
> "You should stop spending on food."

Use:
> "Food spending is 18% above your recent monthly average. Review transactions or adjust your category plan."

## 8. Analytics requirements

Track:
- onboarding_started
- onboarding_completed
- import_started
- import_completed
- transaction_categorized
- category_corrected
- recurring_expense_reviewed
- budget_created
- savings_goal_created
- checkin_viewed
- action_completed
- data_deleted

## 9. Success metrics

Primary:
**Weekly Actionable Financial Check-ins**

Secondary:
- activation
- week-4 retention
- category correction rate
- budget adoption
- savings-goal adoption
- import success rate

Guardrails:
- privacy complaints
- data deletion failures
- malformed import rate
- misleading-insight reports

## 10. Dependencies

- design
- data parsing
- categorization logic
- analytics instrumentation
- privacy review
- security review

## 11. Risks

See `11-risk/risk-register.md`.

## 12. Launch criteria

- critical flows tested
- privacy copy reviewed
- delete/export works
- analytics events validated
- no critical severity defects
- support FAQ ready

## 13. Open questions

1. Does manual CSV import create enough value to drive repeat usage?
2. Which insight is most likely to trigger action?
3. How much automation do users trust?
4. What is the right level of budget flexibility?
5. Will users pay for deeper planning?
