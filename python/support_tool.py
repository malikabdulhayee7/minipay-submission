#!/usr/bin/env python3
import argparse
import json
import logging
import os
import sys
import requests

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

API_BASE_URL = os.getenv("MINIPAY_API_URL", "http://localhost:8080")

def get_transaction(txn_ref: str) -> dict:
    try:
        response = requests.get(f"{API_BASE_URL}/api/transactions/{txn_ref}", timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            logging.error(f"Transaction {txn_ref} not found.")
            sys.exit(1)
        logging.error(f"API error: {e}")
        sys.exit(2)
    except requests.exceptions.RequestException as e:
        logging.error(f"Connection error: {e}")
        sys.exit(3)

def analyze_transaction(data: dict) -> dict:
    anomalies = []
    recommendations = []
    
    if data.get("status") == "PROCESSING":
        anomalies.append("Transaction is stuck in PROCESSING state.")
        recommendations.append("Check downstream payment gateway logs or trigger manual reconciliation.")
    elif data.get("status") == "FAILED":
        anomalies.append("Transaction failed.")
        recommendations.append("Review failure reason and advise customer to retry with a different payment method.")
        
    return {
        "anomalies": anomalies,
        "recommendations": recommendations
    }

def main():
    parser = argparse.ArgumentParser(description="MiniPay L2 Support Tool")
    parser.add_argument("--transaction", required=True, help="Transaction reference ID")
    parser.add_argument("--json", action="store_true", help="Output in JSON format")
    
    args = parser.parse_args()
    
    txn_data = get_transaction(args.transaction)
    analysis = analyze_transaction(txn_data)
    
    report = {
        "transaction_ref": txn_data.get("transaction_ref"),
        "customer_id": txn_data.get("customer_id"),
        "amount": txn_data.get("amount"),
        "status": txn_data.get("status"),
        "created_at": txn_data.get("created_at"),
        "analysis": analysis
    }
    
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"--- MiniPay Transaction Report ---")
        print(f"Reference: {report['transaction_ref']}")
        print(f"Customer ID: {report['customer_id']}")
        print(f"Amount: ${report['amount']}")
        print(f"Status: {report['status']}")
        print(f"Created At: {report['created_at']}")
        print(f"Anomalies: {', '.join(report['analysis']['anomalies']) or 'None'}")
        print(f"Recommendation: {', '.join(report['analysis']['recommendations']) or 'No action required.'}")
        print(f"----------------------------------------------------------")
        
    sys.exit(0)

if __name__ == "__main__":
    main()