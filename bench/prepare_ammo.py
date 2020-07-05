import random

ACCOUNTS = 1000
GET_RATE = 0.2


def request(method, url, headers=[], tag=None):
    req = '\r\n'.join([f'{method} {url} HTTP/1.0', *headers, '', ''])
    return f'{len(req)}\n{req}'


def main():
    accs = list(range(1, ACCOUNTS+1))
    for _ in range(ACCOUNTS*100):
        if random.random() < GET_RATE:
            acc = random.choice(accs)
            print(request('GET', f'/api/account-balance?account={acc}', tag='get-balance'), end='')
        else:
            acc1, acc2 = random.sample(accs, 2)
            amount = random.randint(1, 5)
            print(request('POST', f'/api/transfer?from={acc1}&to={acc2}&amount={amount}', tag='transfer'), end='')


if __name__ == '__main__':
    main()
