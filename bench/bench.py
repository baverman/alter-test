import time
import random

import config
config.DB_PATH = './bench.db'

import accounts

accounts.create_tables(drop=True)
accounts.create_account(1, 0)
accounts.create_account(2, 0)


def do_transaction():
    amount = random.randint(-100, 100)
    accounts.move_money(1, 2, amount)
