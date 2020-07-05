ACCOUNTS = 1000
INITIAL = 100000


def main():
    from bank import accounts
    accounts.create_tables(drop=True)
    for it in range(1, ACCOUNTS+1):
        accounts.create_account(it, INITIAL)


if __name__ == '__main__':
    main()
