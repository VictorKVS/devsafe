# DevSafe — System Guardrails (v1.1)

Version: 1.1  
Status: ENFORCED  
Owner: Viktor Kulichenko  
Date: 2026-01-01  
Related:
- THREATS.md (v1.1)
- TRACEABILITY.md (v1.1)
- 02_TESTS.md
- ADR-0001-devsafe.md

---

## 1. Purpose

Guardrails define **hard boundaries** for DevSafe behavior.

> DevSafe is a developer guardrail, not an autonomous system.  
> If safety cannot be guaranteed — DevSafe must **fail safe**.

These rules must be:
- **enforced in code**
- **testable**
- **visible in UX**

Violation of a guardrail = **BUG**.

---

## 2. Core Safety Principle (Fail-Safe)

### GR-FAILSAFE-01 (MUST)
If DevSafe cannot guarantee safe operation, it MUST:
1) **pause automation** for the active project  
2) **surface the failure** in UI/logs  
3) **not continue** in an unknown/undefined state

**Examples that trigger fail-safe:**
- backup path unavailable
- backup failure
- git repository unsafe state (rebase/merge/conflict)
- push fails repeatedly (configurable threshold) AND user opted-in for strict mode

**Threat coverage:** T1, T2, T6  
**Verification:** E2E tests + visible UI state

---

## 3. Absolute Prohibitions (MUST NOT)

### GR-DATA-01 (MUST NOT)
DevSafe MUST NOT delete user files, ever.
- no cleanup of project files
- no auto-pruning
- no auto-rollback

**Threat coverage:** T1  
**Verification:** Unit: ensure no delete operations are called

---

### GR-GIT-01 (MUST NOT)
DevSafe MUST NOT perform destructive git operations:
- `git reset --hard`
- `git rebase`
- `git merge`
- `git push --force` / `--force-with-lease`

**Threat coverage:** T2  
**Verification:** Unit: disallow commands list

---

### GR-SCOPE-01 (MUST NOT)
DevSafe MUST NOT operate outside the selected active project path.
- no parent directory traversal
- no backup outside configured destination

**Threat coverage:** T7  
**Verification:** Unit: path normalization + containment check

---

### GR-SECRETS-01 (MUST NOT)
DevSafe MUST NOT commit secrets:
- `.env`, `.env.*`
- `*.key`, `*.pem`
- known token patterns (future expansion)

**Threat coverage:** T3  
**Verification:** Unit: deny-list & pattern tests

---

## 4. Mandatory Checks (MUST)

### GR-GITSTATE-01 (MUST)
Before any commit/push, DevSafe MUST verify repository safety:
- no rebase in progress
- no merge in progress
- no conflicts
- not detached HEAD (unless explicitly allowed in settings)

If unsafe → trigger **fail-safe**.

**Threat coverage:** T2  
**Verification:** Unit tests with repo fixtures

---

### GR-BACKUP-01 (MUST)
Before backup, DevSafe MUST verify:
- backup path exists OR can be created
- backup path is writable
- backup destination is not inside project folder (avoid recursion)

If check fails → trigger **fail-safe**.

**Threat coverage:** T1, T6  
**Verification:** Unit: invalid path, recursion prevention

---

### GR-ORDER-01 (MUST)
DevSafe MUST enforce operation order:
1) commit (if changes exist)
2) push (best-effort unless strict mode)
3) backup (after commit)

Backup MUST NOT run before commit.

**Threat coverage:** T1  
**Verification:** Unit: order test

---

### GR-DEBOUNCE-01 (MUST)
DevSafe MUST debounce filesystem events:
- default debounce window: 5–10 seconds
- must prevent commit storms from autosave

**Threat coverage:** T4  
**Verification:** Unit: rapid events -> one commit

---

### GR-SINGLEACTIVE-01 (MUST)
DevSafe MUST allow only one active project at a time.
- max registry size: 5
- only one watcher running

**Threat coverage:** T5  
**Verification:** Unit: activation exclusivity

---

## 5. UX Guardrails (Visibility)

### GR-UX-STATUS-01 (MUST)
DevSafe MUST expose operation statuses clearly:
- Commit: OK / SKIPPED / FAILED
- Push: OK / FAILED
- Backup: OK / FAILED
- Automation: ACTIVE / PAUSED / STOPPED

**Threat coverage:** T6  
**Verification:** UX checklist + E2E

---

### GR-UX-NOSILENT-01 (MUST)
DevSafe MUST NOT fail silently.
- any failure -> log + UI indicator

**Threat coverage:** T6  
**Verification:** E2E: simulate failures

---

## 6. Enforcement Mechanisms (How we enforce)

Guardrails are enforced via:

### 6.1 Code-Level Enforcement
- centralized command executor with deny-list
- centralized path validator (project containment)
- git state inspector
- fail-safe state machine

### 6.2 Test-Level Enforcement
- unit tests for:
  - git unsafe states
  - deny-list secrets
  - path containment
  - debounce
  - operation ordering
- E2E tests for:
  - network down push
  - invalid backup path
  - backup interruption

### 6.3 CI Enforcement (planned)
- block merge if:
  - guardrail tests fail
  - threat-linked issues closed without verification evidence

---

## 7. Guardrail Traceability

| Guardrail | Threats |
|----------|---------|
| GR-FAILSAFE-01 | T1, T2, T6 |
| GR-SECRETS-01 | T3 |
| GR-DEBOUNCE-01 | T4 |
| GR-SINGLEACTIVE-01 | T5 |
| GR-SCOPE-01 | T7 |

---

## 8. Change Policy

Any change to guardrails requires:
- ADR update (new ADR or ADR amendment)
- update to THREATS.md / TRACEABILITY.md if affected
- test updates

---

## 9. Summary

DevSafe is safe because:
- it has strict boundaries
- failures are visible
- automation pauses on uncertainty
- mitigations are testable

Guardrails are **not documentation** — they are **product constraints**.

---
