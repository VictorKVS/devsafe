## DevSafe — Threat Model

Version: 1.1  
Status: ACTIVE  
Owner: Viktor Kulichenko  
Date: 2026-01-01  

Related:
- GUARDRAILS.md (v1.1)
- TRACEABILITY.md (v1.1)
- ADR-0002-failsafe-state-machine.md

---

## 1. Purpose

This document defines a structured threat model for DevSafe.

Its purpose is to identify risks that may lead to:
- loss of source code
- corruption of Git repositories
- unsafe automation behavior
- false sense of safety for developers

Threat modeling is used as a **design control mechanism**,  
not as a theoretical exercise.

---

## 2. Threat Metadata Model

Each threat is described using:

- **Threat ID**
- **Scenario ID**
- **Category**
- **Probability:** Low / Medium / High
- **Impact:** Low / Medium / High
- **Mitigations**
- **Status:** Open / Mitigated / Accepted

---

## 3. Threat Categories & Scenarios

---

### T1 — Data Loss

**Category:** Integrity / Availability  
**Probability:** Medium  
**Impact:** High  
**Status:** Mitigated

#### Scenarios
- **T1.1** Backup process interrupted (robocopy / shutil)
- **T1.2** Commit created but backup not updated
- **T1.3** Backup overwrites valid files with corrupted ones

#### Mitigations
- **M1.1** Backup executed only *after successful commit*
- **M1.2** Backup operations are logged
- **M1.3** Backup path validated before execution
- **M1.4** `.git` directory is never touched by backup engine

---

### T2 — Git Repository Corruption

**Category:** Integrity  
**Probability:** Medium  
**Impact:** High  
**Status:** Mitigated

#### Scenarios
- **T2.1** Auto-commit during `git rebase`
- **T2.2** Auto-commit during merge conflict
- **T2.3** Detached HEAD state

#### Mitigations
- **M2.1** Pre-check git state (`git status`)
- **M2.2** Block commit during rebase / merge / conflict
- **M2.3** Allow commit only on safe branch state

---

### T3 — Secret Leakage

**Category:** Confidentiality  
**Probability:** Medium  
**Impact:** High  
**Status:** Mitigated

#### Scenarios
- **T3.1** Accidental commit of `.env`
- **T3.2** Commit of API keys / tokens
- **T3.3** Misconfigured `.gitignore`

#### Mitigations
- **M3.1** Strict deny-list:
  - `.env`, `.env.*`
  - `*.key`, `*.pem`
- **M3.2** DevSafe never bypasses `.gitignore`
- **M3.3** Optional allow-list (future)
- **M3.4** Optional secret scanners (v0.3+)

---

### T4 — Commit Storm

**Category:** Availability  
**Probability:** High  
**Impact:** Medium  
**Status:** Mitigated

#### Scenarios
- **T4.1** IDE autosave triggers frequent commits
- **T4.2** Watcher reacts to each filesystem event

#### Mitigations
- **M4.1** Debounce ≥ 5 seconds
- **M4.2** Single commit per change window
- **M4.3** Minimum interval between commits

---

### T5 — Resource Exhaustion

**Category:** Availability  
**Probability:** Medium  
**Impact:** Medium  
**Status:** Mitigated

#### Scenarios
- **T5.1** Large project monitored
- **T5.2** Recursive filesystem events
- **T5.3** Heavy backup operations

#### Mitigations
- **M5.1** Only one active project allowed
- **M5.2** Exclude heavy directories
- **M5.3** Backup only after commit

---

### T6 — False Sense of Safety

**Category:** UX / Trust  
**Probability:** Medium  
**Impact:** High  
**Status:** Mitigated

#### Scenarios
- **T6.1** User assumes everything is saved
- **T6.2** GitHub push fails silently
- **T6.3** Invalid backup path unnoticed

#### Mitigations
- **M6.1** Explicit status reporting (Commit / Push / Backup)
- **M6.2** Errors always visible in UI
- **M6.3** Silent failures forbidden
- **M6.4** Fail-safe pause on uncertainty

---

### T7 — Unauthorized Execution

**Category:** Integrity / Execution  
**Probability:** Low  
**Impact:** High  
**Status:** Partial

#### Scenarios
- **T7.1** Malicious git hooks execution
- **T7.2** Watcher monitors injected malicious files
- **T7.3** DevSafe launched from untrusted context

#### Mitigations
- **M7.1** Explicit user enable/disable of automation
- **M7.2** Strict project path containment
- **M7.3** Integrity checks (planned, v0.3+)

---

## 4. Fail-Safe Principle

> If DevSafe cannot guarantee safety,  
> it MUST pause automation and notify the user.

Fail-safe applies to:
- backup failures
- unsafe git state
- invariant violations

---

## 5. Out of Scope Threats (Accepted)

- ransomware
- malware
- root-level attacker
- disk firmware failure

DevSafe is a **developer guardrail**, not a security product.

---

## 6. Summary

This threat model ensures that DevSafe evolves as a:
- predictable
- auditable
- fail-safe automation system

Threat modeling is treated as an **engineering control**,  
not documentation overhead.

---
