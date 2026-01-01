## Fail-Safe State Machine

DevSafe automation is governed by explicit states:

- S0 — STOPPED
- S1 — ACTIVE
- S2 — PAUSED (fail-safe)
- S3 — RECOVERING

All guardrail tests assume compliance with ADR-0002.
Any bypass of state machine is considered a bug.
