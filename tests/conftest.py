import pytest

from bank import config
config.DB_PATH = '/tmp/data.db'


@pytest.fixture(autouse=True)
def make_tables():
    from bank import accounts
    accounts.create_tables(drop=True)
