import psycopg
from datetime import datetime,timezone
with psycopg.connect("host=localhost dbname=pelis user=dam_app password=1234") as conn:
    with conn.cursor() as cur:
        cur.execute("""
CREATE TABLE audit (
audit_id serial PRIMARY KEY,
user_id integer,
resource varchar(500),
time timestamp,
CONSTRAINT FK_aud_use
FOREIGN KEY(user_id)
REFERENCES accounts(user_id))
""")
        
