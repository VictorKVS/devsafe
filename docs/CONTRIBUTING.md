
markdown
Копировать код
# Contributing to DevSafe

Thank you for your interest in contributing to DevSafe.

DevSafe is a **safety-first developer automation system**.
Contributions are welcome, but must follow strict architectural
and safety rules.

---

## 1. Core Principles

By contributing, you agree that:

- Safety is not optional
- Guardrails are non-negotiable
- Silent failures are bugs
- Automation must fail safe

> If safety cannot be guaranteed, DevSafe must pause — not proceed.

---

## 2. Contribution Flow (MANDATORY)

All changes MUST follow this flow:

1. Create a **feature branch** (no direct pushes to `main`)
2. Open a **Pull Request**
3. Ensure **CI checks pass**
4. Obtain required **reviews**
5. Merge via PR only

Direct pushes to `main` are **forbidden**.

---

## 3. Branch & CI Rules

### Branch protection
- `main` branch is protected
- PR is required for every change
- CI guardrails must pass
- Failing guardrails = merge blocked

### CI enforcement
Every PR must pass:
- Guardrails tests
- Fail-Safe state checks
- Structural safety checks

---

## 4. Guardrails & Safety Contracts

The following documents define **hard system constraints**:

- `docs/devsafe/GUARDRAILS.md`
- `docs/devsafe/THREATS.md`
- `docs/devsafe/TRACEABILITY.md`
- `docs/devsafe/ADR-0002-failsafe-state-machine.md`

Any change that violates these documents is considered a **BUG**.

If your change affects safety behavior:
- update the relevant document
- update or add tests
- reference the change in the PR description

---

## 5. Tests Requirements

### Mandatory rules
- New behavior → new tests
- Safety logic → guardrails tests
- State changes → fail-safe state tests

PRs that reduce safety coverage will be rejected.

---

## 6. Code Ownership & Reviews

Critical areas require owner review:
- `docs/devsafe/`
- `tests/guardrails/`
- `.github/workflows/`

CODEOWNERS are enforced for these paths.

---

## 7. Issues & Planning

Before starting work:
- Check existing Issues
- Prefer creating an Issue before large changes
- Reference Issue ID in PR title or description

---

## 8. Commit & PR Guidelines

### Commits
- Clear, descriptive messages
- One logical change per commit
- No "fix stuff" or "WIP" in `main`

### Pull Requests
PR description should include:
- What was changed
- Why it was changed
- Which guardrails / threats are affected
- How it was tested

---

## 9. Scope Boundaries

DevSafe is NOT:
- a malware protection tool
- a ransomware defense system
- a full security platform

DevSafe IS:
- a developer safety guardrail
- a fail-safe automation controller

---

## 10. Final Note

Contributions that improve:
- safety
- determinism
- transparency
- testability

are always welcome.

Contributions that weaken safety guarantees will not be accepted.

---

**DevSafe philosophy:**  
> Automation is allowed only when safety is proven.