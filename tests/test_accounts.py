from bank import accounts


def test_move_money():
    accounts.create_account(1, 100)
    accounts.create_account(2, 200)
    accounts.transfer(1, 2, 50)
    assert accounts.get_balance(1) == 50
    assert accounts.get_balance(2) == 250
