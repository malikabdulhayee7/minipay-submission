# INCIDENT-002 – Application Unavailable After Deployment

**Priority:** P1
**Status:** RESOLVED
**Investigation Date:** 2026-09-16
**Investigator:** Abdul Hayee

## Executive Summary
Following a new release deployment to Kubernetes, the MiniPay application became inaccessible. Pods were running but not ready, and service endpoints were empty. Investigation revealed multiple configuration defects in the provided starter manifest preventing proper traffic routing and health checking.

## Observations & Evidence
- Pods were in `Running` state but `0/1 Ready`.
- `kubectl get endpoints minipay-api -n minipay` returned `<none>` (empty).
- `kubectl describe pod` showed readiness probe failures: `Connection refused` on port 8081.

## Root Causes Identified in Starter Manifest
### Defect 1: Service Selector Mismatch
The Service selector was `app: minipay-backend`, but the Deployment labeled pods with `app: minipay-api`.
**Fix:** Changed Service selector to `app: minipay-api`.

### Defect 2: Service TargetPort Mismatch
The Service `targetPort` was `8081`, but the container explicitly exposed `containerPort: 8080`.
**Fix:** Aligned Service `targetPort` to `8080`.

### Defect 3: Readiness Probe Port Mismatch
The `readinessProbe` was checking port `8081`, while the application health endpoint runs on the main container port (`8080`).
**Fix:** Aligned `readinessProbe` port to `8080`.

## Corrective Action
Applied corrected manifests with aligned selectors, ports, and probes. Added resource requests/limits for production readiness and replaced placeholder image for validation.

## Validation
- `kubectl get pods -n minipay` shows pods as `Running` and `Ready`.
- `kubectl get endpoints` now correctly lists pod IPs.
- Service successfully routes traffic to the backend pods.

## Preventive Controls
1. **CI/CD Validation:** Use `kubeconform` or `kubeval` in the pipeline to validate manifest schemas and label consistency before deployment.
2. **Automated Smoke Tests:** Run post-deployment curl tests against the service endpoint to verify routing.
3. **GitOps:** Use ArgoCD/Flux to detect configuration drift and enable easy rollbacks.
