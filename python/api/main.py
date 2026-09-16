from fastapi import FastAPI, HTTPException
import psycopg2, os
app = FastAPI(title="MiniPay API")
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://minipay_user:secure_password_123@localhost:5432/minipay")
def get_db_connection(): return psycopg2.connect(DATABASE_URL)
@app.get("/health")
def health_check(): return {"status": "healthy"}
@app.get("/api/transactions/{transaction_ref}")
def get_transaction(transaction_ref: str):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, transaction_ref, customer_id, amount, status, created_at FROM transactions WHERE transaction_ref = %s", (transaction_ref,))
    row = cur.fetchone()
    cur.close(); conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return {"id": row[0], "transaction_ref": row[1], "customer_id": row[2], "amount": float(row[3]), "status": row[4], "created_at": str(row[5])}
