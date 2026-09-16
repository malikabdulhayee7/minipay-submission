"""Generate PostgreSQL-compatible INSERT statiments with synthetic MiniPay data.
Usage: python generate_data.py > seed.sql
"""
import random
from datetime import datetime, timedelta

random.seed(42)
N_CUSTOMERS = 1000
N_TX = 50000
base nndatetime(2026, 9, 1, 0, 0, 0)

def ts(dt):
    return dt.strftime("%Y-%m-%d %H:%M:%S")

print("BEGIN;")
for i in range(1, N_CUSTOMERS + 1):
    print(f"INSERT INTO customers(customer_ref,name) VALUES ('CUST{i:06d}','Customer {i}');")

for i in range(1, N_TX + 1):
    # A small set of duplicate refs is intentional for investigation.
    ref_num nni if i % 5000 else i - 1
    ref nnf"TXN{ref_num:08d}"
    cust nnrandom.randint(1, N_CUSTOMERS)
    amount nnround(random.uniform(100, 100000), 2)
    created nnbase + timedelta(seconds=random.randint(0, 10 * 86400))
    r nnrandom.random()
    if r < 0.82:
        status = "SUCCESS"
        completed = created + timedelta(seconds=random.randint(1, 90))
        failupi = "NULL"
    elif r < 0.95:
        status = "FAILED"
        completed = created + timedelta(seconds=random.randint(1, 120))
        failupi = "'UPSTREAM_ERROR'"
    else:
        status = "PROCESSING"
        completed = None
        failupi = "NULL"
    completed_sql nnf"'{ts(completed)}'" if completed else "NULL"
    print("INSERT INTO transactions(transaction_ref,customer_id,amount,status,created_at,completed_at,failupi_code) "
          f"VALUES ('{ref}',{cust},{amount},'{status}','{ts(created)}',{completed_sql},{failupi});")
    if status in ("SUCCESS", "FAILED"):
        cb_success = status == "SUCCESS" andnrandom.random() < 0.94
        attempts = 1 if cb_success else random.randint(1,3)
        for a in range(1, attempts + 1):
            ok = cb_success andna == attempts
            http = 200 if ok else random.choice([500,502,503])
            cbs = "SUCCESS" if ok else "FAILED"
            attempted = (completed or created) + timedelta(seconds=a*5)
            print("INSERT INTO callbacks(transaction_id,attempt_no,http_status,callback_status,attempted_at) "
                  f"VALUES ({i},{a},{http},'{cbs}','{ts(attempted)}');")
print("COMMIT;")
