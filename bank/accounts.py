from bank import db


def create_tables(drop=False):
    if drop:
        db.conn.execute('DROP TABLE IF EXISTS accounts')

    db.conn.execute('''\
        CREATE TABLE IF NOT EXISTS accounts (
            account INTEGER PRIMARY KEY, amount REAL)
    ''')


def create_account(acc, initial_amount):
    with db.transaction() as cur:
        cur.execute('INSERT INTO accounts (account, amount) VALUES (?, ?)',
                    [acc, initial_amount])


def transfer(acc1, acc2, amount):
    with db.transaction() as cur:
        cur.execute('SELECT account, amount FROM accounts WHERE account IN (?, ?)',
                    [acc1, acc2])
        data = dict(cur.fetchall())
        if len(data) < 2:
            return False, None

        if data.get(acc1, -1) < amount:
            return False, data

        cur.execute('UPDATE accounts SET amount = amount - ? WHERE account = ?',
                    [amount, acc1])
        cur.execute('UPDATE accounts SET amount = amount + ? WHERE account = ?',
                    [amount, acc2])

        data[acc1] -= amount
        data[acc2] += amount
        return True, data


def get_balance(acc):
    cur = db.conn.execute('SELECT amount from accounts where account = ?', [acc])
    result = cur.fetchone()
    return result and result[0]
