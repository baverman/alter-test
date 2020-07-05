import sqlite3
from contextlib import contextmanager
from threading import get_ident

from bank import config

_conn = {}


def conn():
    try:
        return _conn[get_ident()]
    except KeyError:
        pass
    c = _conn[get_ident()] = sqlite3.connect(
        config.DB_PATH, isolation_level=None)
    c.execute('pragma journal_mode=wal')
    c.execute('pragma cache_size=-50000')
    c.execute('pragma busy_timeout=5000')
    c.execute('pragma synchronous=1')
    return c


@contextmanager
def transaction():
    cn = conn()
    cur = cn.cursor()
    cur.execute('BEGIN IMMEDIATE')
    try:
        yield cur
    except:
        if cn.in_transaction:
            cn.rollback()
        raise
    else:
        if cn.in_transaction:
            cn.commit()
    finally:
        cur.close()
