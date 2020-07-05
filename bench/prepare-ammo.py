import random

ACCOUNTS = 1000
INITIAL = 100000


def request(method, url, headers=[]):
    req = '\r\n'.join([f'{method} {url} HTTP/1.0', *headers, '', ''])
    return f'{len(req)}\n{req}'


def main():
    import accounts
    accounts.create_tables(drop=True)

    accs = list(range(1, ACCOUNTS+1))
    for it in accs:
        accounts.create_account(it, 1000000)

    for _ in range(ACCOUNTS*100):
        if random.random() < 0.1:
            acc = random.choice(accs)
            print(request('GET', f'/api/account-balance?account={acc}'), end='')
        else:
            acc1, acc2 = random.sample(accs, 2)
            amount = random.randint(1, 5)
            print(request('POST', f'/api/transfer?from={acc1}&to={acc2}&amount={amount}'), end='')


if __name__ == '__main__':
    main()
