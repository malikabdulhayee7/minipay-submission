# AI Usage Report

This document details the strategic use of AI tools during this technical assessment, focusing on complex engineering tasks and validation of AI-generated solutions.

## Tools Used
- **LLMs (ChatGPT-4 / Claude 3.5 Sonnet):** Used strictly for architectural reasoning, complex debugging, and interpreting system-level outputs.

## Complex Tasks Assisted by AI (Evaluated Areas)

### 1. Kubernetes Manifest Defect Analysis (INCIDENT-002)
- **AI Role:** Assisted in systematically cross-referencing the provided starter manifest against Kubernetes networking and health-check best practices.
- **Outcome:** Helped pinpoint the exact 3 compounding defects: Service selector mismatch (`minipay-backend` vs `minipay-api`), `targetPort` misalignment, and `readinessProbe` port discrepancy.

### 2. Database Query Optimization & EXPLAIN ANALYZE Interpretation (INCIDENT-003)
- **AI Role:** Used to formulate the optimal composite B-tree index strategy (`status`, `created_at`) for the specific L2 support query pattern.
- **Outcome:** Assisted in interpreting the `EXPLAIN ANALYZE` output to clearly demonstrate the shift from a costly `Seq Scan` to an efficient `Bitmap Index Scan`, providing concrete before/after execution time metrics.

### 3. Python CLI Tool Architecture (Support Utility)
- **AI Role:** Guided the design of robust error handling, specifically implementing proper `sys.exit()` codes, request timeout management, and structured JSON serialization for machine-readable output.

## Validation of AI Output
- **Logic Verification:** All AI-suggested Kubernetes configurations were cross-referenced with official Kubernetes documentation regarding `selector` and `probe` behaviors before application.
- **Security & Best Practices:** Reviewed all generated Python code to ensure no hardcoded credentials were used (enforced environment variable usage for DB URLs).
- **Empirical Testing:** AI-suggested SQL indexes were empirically tested using `EXPLAIN ANALYZE` on a 50,000+ row dataset to prove actual performance gains, rather than blindly accepting theoretical advice.

## Example of AI Correction / Material Improvement (Crucial)
- **Task:** Generating the initial FastAPI transaction lookup endpoint.
- **Initial AI Output:** The AI generated code that directly accessed `row[0]` without checking if the query returned a result. This would cause a `TypeError: 'NoneType' object is not subscriptable` for invalid IDs.
- **My Correction:** I manually reviewed the logic, recognized the missing null-check, and **rejected** the AI's direct array access. I modified the code to explicitly `raise HTTPException(status_code=404)` when `row is None`.
- **Result:** This material improvement directly resolved INCIDENT-001, demonstrating proper production-grade error handling over blind AI acceptance.

## Engineering Ownership
While AI accelerated the debugging of complex system interactions, all final architectural decisions (e.g., choosing the specific composite index, designing CLI exit codes, and structuring incremental Git commits) were made, validated, and owned by me. I am fully prepared to explain, modify, or troubleshoot any part of this repository during the follow-up interview.