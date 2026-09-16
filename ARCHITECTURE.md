# MiniPay System Architecture

## Overview
MiniPay is a small enterprise-style payment processing application consisting of a REST API and a relational database, designed to be deployed and operated in a Kubernetes environment.

## Components
1. **API Layer (FastAPI)**: Handles transaction lookups, health checks, and business logic. Designed with robust error handling (e.g., proper 404 responses for missing resources).
2. **Data Layer (PostgreSQL)**: Relational database storing `customers` and `transactions`. Optimized with composite indexes (e.g., `idx_txn_status_created`) for high-volume L2 support queries.
3. **Orchestration (Kubernetes/K3s)**: Manages deployment, scaling, and health checks (liveness/readiness probes) for the API layer.

## Design Decisions
- **Health Checks**: Implemented strict readiness and liveness probes to prevent traffic routing to unhealthy pods (resolving INCIDENT-002).
- **Error Handling**: API explicitly checks for `None` results from DB queries to prevent `TypeError` crashes (resolving INCIDENT-001).
- **Performance**: Added targeted B-tree indexes to eliminate costly Sequential Scans on large datasets (resolving INCIDENT-003).
- **Security**: No hardcoded credentials; database URLs are managed via environment variables.