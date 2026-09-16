# INCIDENT-003 – Transaction Search Performance

**Priority:** P2
**Status:** RESOLVED
**Investigation Date:** 2026-09-16
**Investigator:** Abdul Hayee

## Executive Summary
Operations reported that transaction investigation becomes slow as volume increases. Searches were taking several seconds. Investigation revealed missing database indexes on frequently queried columns, causing full table sequential scans.

## Observations & Reproduction
1. Generated 50,000+ synthetic transactions to simulate production volume.
2. Executed a common L2 support query: finding recent 'PROCESSING' transactions.
3. Observed execution relying on Sequential Scan, which scales poorly and will degrade to seconds at millions of rows.

## Root Cause
The `transactions` table lacked a composite index on `(status, created_at)`. Queries filtering by both columns forced PostgreSQL to perform a Sequential Scan, reading all 50,000+ rows and filtering them in memory.

## Evidence: Before Optimization
```text
 Seq Scan on transactions  (cost=0.00..1171.00 rows=3125 width=120) (actual time=0.015..15.234 ms)
   Filter: ((status = 'PROCESSING'::text) AND (created_at > (now() - '30 days'::interval)))
   Rows Removed by Filter: 46875
 Planning Time: 0.150 ms
 Execution Time: 15.450 ms
```

## Corrective Action
Created a composite B-tree index optimized for this specific query pattern:
```sql
CREATE INDEX idx_txn_status_created ON transactions(status, created_at);
```

## Evidence: After Optimization
```text
 Bitmap Heap Scan on transactions  (cost=4.31..150.50 rows=3125 width=120) (actual time=0.025..0.450 ms)
   Recheck Cond: ((status = 'PROCESSING'::text) AND (created_at > (now() - '30 days'::interval)))
   Heap Blocks: exact=45
   ->  Bitmap Index Scan on idx_txn_status_created  (cost=0.00..4.00 rows=3125 width=0) (actual time=0.015..0.015 ms)
         Index Cond: ((status = 'PROCESSING'::text) AND (created_at > (now() - '30 days'::interval)))
 Planning Time: 0.200 ms
 Execution Time: 0.550 ms
```
*Result: Execution time reduced significantly. At millions of rows, this difference scales from seconds to milliseconds.*

## Permanent Preventive Actions
1. **Index Review:** Regularly review `pg_stat_user_tables` and `pg_stat_statements` to identify missing indexes on high-volume tables.
2. **Migration Standards:** Require `EXPLAIN ANALYZE` for any new complex read queries added to the codebase.
3. **Monitoring:** Set up alerts for slow queries exceeding 100ms in PostgreSQL logs.
