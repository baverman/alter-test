from bank import db
from sqlite3 import IntegrityError


def create_tables(drop=False):
    if drop:
        db.conn().execute('DROP TABLE IF EXISTS accounts')

    db.conn().execute('''\
        CREATE TABLE IF NOT EXISTS accounts (
            account INTEGER PRIMARY KEY,
            amount REAL,
            CHECK(amount > 0)
        )
    ''')


def create_account(acc, initial_amount):
    try:
        with db.transaction() as cur:
            cur.execute('INSERT INTO accounts (account, amount) VALUES (?, ?)',
                        [acc, initial_amount])
    except IntegrityError:
        return False

    return True


def transfer(acc1, acc2, amount):
    acc1_updated = False
    with db.transaction() as cur:
        try:
            cur.execute('UPDATE accounts SET amount = amount - ? WHERE account = ?',
                        [amount, acc1])
            acc1_updated = cur.rowcount > 0
        except IntegrityError:
            cur.connection.rollback()
        else:
            if acc1_updated:
                cur.execute('UPDATE accounts SET amount = amount + ? WHERE account = ?',
                            [amount, acc2])
                if not cur.rowcount:
                    cur.connection.rollback()

        cur.execute('SELECT account, amount FROM accounts WHERE account IN (?, ?)',
                    [acc1, acc2])

        data = dict(cur.fetchall())

    if len(data) < 2:
        return False, None

    return acc1_updated, data


def get_balance(acc):
    cur = db.conn().execute('SELECT amount from accounts where account = ?', [acc])
    result = cur.fetchone()
    return result and result[0]
