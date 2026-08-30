# Acceptance Criteria

## CSV Import

**Given** a supported CSV  
**When** the user selects it  
**Then** the product shows a preview before persistence.

**Given** malformed rows  
**When** validation runs  
**Then** invalid rows are identified with human-readable reasons.

## Categorization

**Given** a transaction with a known merchant rule  
**When** categorization runs  
**Then** a category is assigned.

**Given** a user changes a category  
**When** they save the correction  
**Then** the displayed category and downstream summary update.

## Cash Flow

**Given** valid transactions for a month  
**When** the dashboard loads  
**Then** income, expense and net cash flow are displayed.

## Weekly Check-in

**Given** a user has sufficient transaction history  
**When** the weekly check-in opens  
**Then** no more than three priority insights are shown.

Each insight must include:
- what changed
- why it matters
- suggested action
- confidence/context where relevant

## Privacy

**Given** a user requests deletion  
**When** deletion is confirmed  
**Then** stored financial records are removed and the UI confirms completion.

## Guardrail

The product must not present investment, tax, lending or credit recommendations as personalized financial advice.
