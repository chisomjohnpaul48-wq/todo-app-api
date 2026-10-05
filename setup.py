from database import pool

def init_table():
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS todos (
                    id SERIAL PRIMARY KEY,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL,
                    completed BOOLEAN NOT NULL DEFAULT FALSE
                )
            """)
            conn.commit()