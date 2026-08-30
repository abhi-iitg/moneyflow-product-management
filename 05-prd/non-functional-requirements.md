# Non-Functional Requirements

## Privacy

- minimize collected data
- explain purpose before collection
- allow deletion/export
- do not store bank passwords or OTPs
- use synthetic data in demonstrations

## Security

- encryption in transit and at rest in production
- secure authentication
- least-privilege access
- audit logging
- secrets outside source control

## Performance

- initial dashboard target: <2 seconds for a normal demo dataset
- import validation feedback: <5 seconds for 10,000 rows

## Reliability

- failed imports must not corrupt existing data
- calculations should be deterministic for identical input
- product should surface uncertainty instead of silently fabricating values

## Accessibility

- keyboard-accessible critical flows
- readable contrast
- clear error messages
- charts must have text alternatives
