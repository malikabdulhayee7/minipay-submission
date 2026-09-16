# INCIDENT-001 – Intermittent Transaction Search Failure

**Priority:** P2
  
**Status:** RESOLVED
  
**Investigation Date:** 2026-09-16  
**Investigator:** Abdul Hayee

## Executive Summary
Users reported intermittent HTTP 500 errors when searching for transactions. Investigation revealed that the API code did not properly handle cases where a transaction ID does not exist in the database, causing unhandled `TypeError` exceptions.

## Observations & Reproduction
- Valid transaction searches returned HTTP 200 with data.
- Non-existent transaction searches returned HTTP 500 Internal Server Error.
- Application logs showed: `TypeError: 'NoneType' object is not subscriptable`.

## Root Cause
The API endpoint `/api/transactions/{transaction_ref}` assumed `cursor.fetchone()` would always return a result. When a transaction did not exist, it returned `None`. The code then attempted to access `row[0]`, triggering a `TypeError` instead of returning a proper HTTP 404 Not Found response.

## Immediate Corrective Action
Added a null-check before accessing the row data:
```python
if not row:
    raise HTTPException(status_code=404, detail="Transaction not found")
```

## Validation
- `curl http://localhost:8080/api/transactions/TXN999999` now correctly returns HTTP 404.
- Valid transactions continue to return HTTP 200.
- No more `TypeError` exceptions in application logs.

## Permanent Preventive Actions
1. **Comprehensive Error Handling**: Enforce null-checks for all database query results in code reviews.
2. **Automated Testing**: Add pytest unit tests covering negative scenarios (e.g., searching for non-existent IDs).
3. **Monitoring**: Alert on sudden spikes in HTTP 5xx errors via application logging.
