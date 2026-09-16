# Setup and Reproduction Instructions

## Prerequisites
- Ubuntu 22.04/24.04 LTS (or similar Linux environment)
- Python 3.10+
- PostgreSQL 14+
- Kubernetes (K3s, Minikube, or Kind)

## 1. Database Setup
```bash
sudo -u postgres psql -c "CREATE USER minipay_user WITH PASSWORD 'secure_password_123';"
sudo -u postgres psql -c "CREATE DATABASE minipay OWNER minipay_user;"
sudo -u postgres psql -d minipay -f sql/schema.sql
```

## 2. API Application Setup
```bash
cd python/api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8080 &
```

## 3. Kubernetes Deployment
```bash
kubectl apply -f kubernetes/manifest.yaml
kubectl get pods -n minipay
```

## 4. Running Tests
```bash
# API Tests
cd tests/api
python3 -m venv venv && source venv/bin/activate
pip install pytest requests
pytest test_api.py -v

# Python Support Tool
cd python
pip install requests
python3 support_tool.py --transaction TXN000123
python3 support_tool.py --transaction TXN000123 --json
```