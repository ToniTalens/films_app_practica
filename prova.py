import psycopg
from datetime import datetime, timezone

dt = datetime.now(timezone.utc)

with psycopg.connect("host=localhost dbname=demo user=dam_app password=1234") as conn:
    with conn.cursor() as cur:
        cur.execute("INSERT INTO accounts (username, password, email, created_at)")