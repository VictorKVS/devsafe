# ADR-0002: Fail-Safe State Machine

Status: ACCEPTED  
Date: 2026-01-01  
Owner: Viktor Kulichenko  
Project: DevSafe  
Related:
- GUARDRAILS.md (v1.1)
- THREATS.md (v1.1)
- TRACEABILITY.md (v1.1)
- ADR-0001-devsafe.md

---

## 1. Context

DevSafe performs automated actions that affect:
- source code history (Git)
- local filesystem (backup)
- developer trust

Failures in these operations may lead to:
- data loss
- corrupted repositories
- false sense of safety

Given this, DevSafe **must not rely on implicit assumptions** about system correctness.

A formal **Fail-Safe State Machine** is required to:
- define allowed system states
- control transitions
- ensure automation halts on uncertainty

---

## 2. Decision

DevSafe SHALL implement an explicit **Fail-Safe State Machine** governing
all automation behavior.

Automation is allowed **only** in safe, verified states.

If safety cannot be guaranteed, DevSafe MUST:
- transition to a paused state
- surface the failure
- await explicit user action

---

## 3. State Definitions

### S0 — STOPPED
**Description:**  
Automation is disabled. No watcher, no git, no backup.

**Entry Conditions:**
- application start
- user manually stops automation
- critical failure without recovery

**Allowed Actions:**
- configure projects
- select active project
- start automation

---

### S1 — ACTIVE
**Description:**  
Automation is running and operating normally.

**Guards (must hold):**
- exactly one active project
- git repository is safe
- backup path is valid
- debounce active

**Allowed Actions:**
- file watching
- commit
- push
- backup

---

### S2 — PAUSED (FAIL-SAFE)
**Description:**  
Automation is paused due to detected risk or failure.

**Triggers:**
- backup failure
- unsafe git state
- repeated push failure (strict mode)
- invalid backup path
- internal invariant violation

**Allowed Actions:**
- show error
- log details
- wait for user decision

**Forbidden Actions:**
- commit
- push
- backup
- watcher execution

---

### S3 — RECOVERING
**Description:**  
System attempts controlled recovery after user intervention.

**Entry Conditions:**
- user acknowledges failure
- preconditions re-validated

**Allowed Actions:**
- re-validate git state
- re-validate backup path
- resume automation if safe

---

## 4. State Transitions

| From | To | Trigger |
|----|----|--------|
| S0 | S1 | User presses "Start" and all guards pass |
| S1 | S2 | Any guardrail violation |
| S2 | S3 | User chooses "Retry / Resume" |
| S3 | S1 | All guards revalidated |
| S3 | S0 | User chooses "Stop" |
| S1 | S0 | User presses "Stop" |

---

## 5. Guardrail Integration

Fail-Safe State Machine enforces the following guardrails:

| Guardrail | Enforcement |
|---------|-------------|
| GR-FAILSAFE-01 | Transition S1 → S2 |
| GR-GITSTATE-01 | Block commit, force S2 |
| GR-BACKUP-01 | Block backup, force S2 |
| GR-UX-NOSILENT-01 | Error surfaced on S2 |
| GR-SINGLEACTIVE-01 | Block S1 entry |

---

## 6. Observability Requirements

State transitions MUST be:
- logged
- visible in UI
- traceable in logs

Example UI states:
- ACTIVE
- PAUSED (reason displayed)
- STOPPED

---

## 7. Consequences

### Positive
- deterministic behavior
- no silent failures
- predictable automation
- easier testing and reasoning

### Trade-offs
- slightly increased complexity
- user interaction required on failure

This trade-off is **intentional** and aligned with DevSafe philosophy.

---

## 8. Enforcement & Testing

State machine MUST be:
- implemented as explicit enum/state object
- unit-tested for all transitions
- covered by E2E fail-safe tests

Any code path bypassing the state machine is a BUG.

---

## 9. Summary

DevSafe automation is governed by **explicit safety states**, not assumptions.

> Automation is allowed only when safety is proven.  
> Uncertainty leads to pause, not blind continuation.

This ADR establishes DevSafe as a **fail-safe-first system**.

---
