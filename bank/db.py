import sqlite3
from contextlib import contextmanager

from bank import config

conn = sqlite3.connect(config.DB_PATH, isolation_level=None)
conn.execute('pragma journal_mode=wal')
conn.execute('pragma cache_size=-50000')
conn.execute('pragma busy_timeout=5000')
conn.execute('pragma synchronous=1')


@contextmanager
def transaction():
    conn.execute('BEGIN IMMEDIATE')
    cur = conn.cursor()
    try:
        yield cur
    except:
        cur.execute('ROLLBACK')
        raise
    else:
        cur.execute('COMMIT')
    finally:
        cur.close()
