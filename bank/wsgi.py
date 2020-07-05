from covador import item, frange
from http import Application, query_string, json_response

import accounts
accounts.create_tables()

app = application = Application()


@app.api('/api/account-balance')
@query_string(account=int)
def account_info(request, account):
    amount = accounts.get_balance(account)
    if amount is None:
        return json_response({'error': 'invalid-account'}, 400)
    else:
        return {'result': amount}


@app.api('/api/create-account')
@query_string(account=int, amount=float)
def create_account(request, account, amount):
    accounts.create_account(account, amount)
    return {'result': 'ok'}


@app.api('/api/transfer/')
@query_string(acc1=item(int, src='from'),
              acc2=item(int, src='to'),
              amount=frange(min=0))
def transfer(request, acc1, acc2, amount):
    transfered, balance = accounts.transfer(acc1, acc2, amount)
    if transfered:
        return {'result': balance}
    elif balance:
        return json_response({'result': balance, 'error': 'insufficient-funds'}, 409)
    else:
        return json_response({'error': 'unknown-account'}, 400)
