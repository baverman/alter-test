import threading
import random

from bank import accounts, db


def test_positive():
    accounts.create_account(1, 100)
    accounts.create_account(2, 200)
    result = accounts.transfer(1, 2, 50)
    assert result == (True, {1: 50, 2: 250})
    assert accounts.get_balance(1) == 50
    assert accounts.get_balance(2) == 250


def test_repeat_create():
    assert accounts.create_account(1, 100)
    assert not accounts.create_account(1, 100)


def test_ivalid_transfer():
    t, b = accounts.transfer(1, 2, 50)
    assert (t, b) == (False, None)

    accounts.create_account(1, 100)
    t, b = accounts.transfer(1, 2, 50)
    assert (t, b) == (False, None)
    assert accounts.get_balance(1) == 100

    accounts.create_account(2, 100)
    t, b = accounts.transfer(1, 2, 150)
    assert (t, b) == (False, {1: 100, 2: 100})
    assert accounts.get_balance(1) == 100
    assert accounts.get_balance(2) == 100


def test_concurrency():
    for it in range(1000):
        accounts.create_account(it, 100000)

    def worker():
        for _ in range(1000):
            acc1 = random.randint(0, 999)
            acc2 = random.randint(0, 999)
            accounts.transfer(acc1, acc2, 1)

    wlist = []
    for _ in range(10):
        t = threading.Thread(target=worker, daemon=True)
        t.start()
        wlist.append(t)

    for t in wlist:
        t.join()

    result, = db.conn().execute('SELECT sum(amount) from accounts').fetchone()
    assert result == 1000 * 100000
