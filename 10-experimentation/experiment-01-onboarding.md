# Experiment E01 — Privacy-First Onboarding

## Hypothesis

If users see a concise explanation of data handling before importing data, then qualified users will have higher import completion because uncertainty is reduced.

## Variants

**Control**
- standard onboarding
- privacy information accessible through secondary link

**Treatment**
- short "How your data is handled" panel
- explicit no-credential-storage statement
- visible delete/export controls

## Primary metric

Import completion rate.

## Secondary metrics

- onboarding completion
- time to first snapshot
- first actionable check-in

## Guardrails

- privacy concern rate
- support contacts about data handling
- abandonment after privacy screen

## Decision rule

Ship treatment if:
- primary metric improves meaningfully,
- confidence interval excludes material harm,
- no trust guardrail worsens beyond predefined threshold.

## Important

This is an **experiment design**, not an experiment result.
