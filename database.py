import os

from dotenv import load_dotenv
from psycopg_pool import ConnectionPool

load_dotenv()

db_url = os.getenv("DATABASE_URL")

if not db_url:
    raise RuntimeError("DATABASE_URL environment variable is not set")

pool = ConnectionPool(
    conninfo=db_url,
    max_size=5,
    min_size=1
)

def get_conn():
    with pool.connection() as conn:
        yield conn