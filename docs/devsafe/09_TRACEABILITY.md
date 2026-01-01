# DevSafe — Threat to Issue Traceability Matrix

Version: 1.1  
Status: ACTIVE  
Owner: Viktor Kulichenko  

---

## 1. Purpose

This document ensures **end-to-end traceability** between:

- identified threats (THREATS.md)
- implementation tasks (GitHub Issues)
- verification mechanisms (tests / observable behavior)

Goal:

> Guarantee that **every critical threat is mitigated by design, code,  
> and verification**, not assumptions.

---

## 2. Coverage Semantics

| Status | Meaning |
|------|--------|
| ✅ Covered | Mitigation implemented **and verified** |
| ⚠️ Partial | Mitigation implemented **without full protection or verification** |
| ⏳ Future | Planned in later versions |

---

## 3. Threat → Issue → Verification Mapping

---

### T1 — Data Loss

| Threat Scenario | Mitigation | Issue | Verification Method |
|----------------|-----------|-------|---------------------|
| T1.1 Backup interrupted | Backup after commit, logging | #6 | E2E: interrupt backup → verify error & no data loss |
| T1.2 Commit w/o backup | Enforced execution order | #6 | Unit: commit triggers backup |
| T1.3 Corrupted overwrite | Validation + logging | #6 | Manual recovery test |
| Fail-safe pause | Stop automation on failure | #8 | E2E: simulate failure → check paused state |

---

### T2 — Git Repository Corruption

| Threat Scenario | Mitigation | Issue | Verification Method |
|----------------|-----------|-------|---------------------|
| T2.1 Commit during rebase | Git state check | #4 | Unit: `test_block_commit_during_rebase` |
| T2.2 Commit on conflict | Conflict detection | #4 | Unit: conflict repo fixture |
| T2.3 Detached HEAD | Branch validation | #4 | Unit: detached HEAD scenario |

---

### T3 — Secret Leakage

| Threat Scenario | Mitigation | Issue | Verification Method |
|----------------|-----------|-------|---------------------|
| T3.1 Commit `.env` | Deny-list enforcement | #4 | Unit: forbidden file commit |
| T3.2 Commit keys | Deny-list enforcement | #4 | Unit: key-pattern detection |
| T3.3 Bad `.gitignore` | Never bypass ignore | #4 | Unit: ignored file untouched |
| Advanced scanners | Secret scanning | ⏳ v0.3 | Planned: gitleaks hook |

---

### T4 — Commit Storm

| Threat Scenario | Mitigation | Issue | Verification Method |
|----------------|-----------|-------|---------------------|
| T4.1 IDE autosave | Debounce | #3 | Unit: rapid events → 1 commit |
| T4.2 Watcher spam | Single window | #3 | Unit: multi-write test |

---

### T5 — Resource Exhaustion

| Threat Scenario | Mitigation | Issue | Verification Method |
|----------------|-----------|-------|---------------------|
| T5.1 Large project | Single active project | #1 | Unit: activate 2nd project fails |
| T5.2 Recursive events | Directory exclusion | #2 | Unit: ignored dirs no events |
| T5.3 Heavy backup | Backup after commit | #6 | E2E: large tree copy |

---

### T6 — False Sense of Safety

| Threat Scenario | Mitigation | Issue | Verification Method |
|----------------|-----------|-------|---------------------|
| T6.1 Assumed safety | Explicit UI status | #7 | UX test: status visible |
| T6.2 Silent push fail | Error logging | #8 | E2E: network down → UI alert |
| T6.3 Invalid backup path | Visible failure | #8 | Unit: invalid path test |

---

### T7 — Unauthorized Execution

| Threat Scenario | Mitigation | Issue | Verification Method |
|----------------|-----------|-------|---------------------|
| T7.1 Malicious git hooks | User-controlled enable | #7 | Manual: hooks present |
| T7.2 File injection | Project scope whitelist | #2 | Unit: external dir ignored |
| T7.3 Untrusted launch | Integrity checks | ⏳ v0.3 | Planned: hash validation |

---

## 4. Rules for Issue Closure (Quality Gate)

An issue linked to a threat **MUST NOT be closed** unless:

- mitigation is implemented
- mitigation behavior is observable
- verification method exists and passes
- implementation matches THREATS.md & GUARDRAILS.md

**Violation = BUG**

---

## 5. Architectural Value

This matrix:

- eliminates forgotten threats
- prevents security theatre
- enables audit & CI enforcement
- turns threat modeling into executable engineering control

---

## 6. Next Evolution

Planned enhancements:
- automated generation from GitHub Issues
- CI gate: block merge if critical threat unverified
- threat-based test coverage report

---