import time
import random

from bank import config
config.DB_PATH = './bench/bench.db'

from bank import accounts

accounts.create_tables(drop=True)
accounts.create_account(1, 10)
accounts.create_account(2, 10)


def do_transaction():
    accounts.transfer(1, 2, 0)
