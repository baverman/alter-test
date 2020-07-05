# Bank

Main idea to fulfill performance requirements was to use SQLite.
It has serializable transactions so we can easily implement fund transfer
semantic (`bank.accounts`):

* Use CHECK constraint on positive account balance to reliably catch
  insufficient funds.
* Use single select to get final state for both accounts in question.

Also I've used a micro lib from another project (`bank.http`) to
eliminate web framework overhead.

## Endpoints

* `POST /api/create-account?account=:acc&amount=:initial`: Create account
  `:acc` with `:initial` amount of funds.
* `GET /api/get-balance?account=:acc`: Get current balance for account `:acc`.
* `POST /api/transfer?from=:acc1&to=:acc2&amount=:amount`: Transfer `:amount`
  of funds from `:acc1` to `:acc2`.

## Setup and run

By default application will listen on `0.0.0.0:8000`.
Path do file with database can be tweaked in `bank.config` module.

### With virtualenv

```
pip install -r requirements.txt
uwsgi --ini etc/uwsgi.ini
```

### With docker-compose

```
docker-compose up
```

## Testing

Install pytest:

```
pip install pytest pytest-cov
```

And run:

```
py.test --cov
```

Tests in `tests/test_accounts.py` verify correct transfer behavior and
consistency in case of concurrent access.


## Performance tuning

Test raw transfer time:

```
python -m timeit -v -s 'from bench.bench import do_transaction as f' 'f()'
```

Test web service:

```
python -m bench.prepare_accounts
python -m bench.prepare_ammo > bench/urls.txt
cd bench
yandex-tank urls.txt
```

Tank results for 300 -> 2000 rps for 120s against live VPS:

```
 Data delay: 4s, RPS: 1,940  ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▅▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇  . Duration: 0:02:00                 ETA: 0:00:00
                                                                                                  . 
 Percentiles (all/last 1m/last), ms:  . HTTP codes:                                               . Hosts: localhost => 172.105.72.118:8000
 100.0% <  67.0  54.0  12.7           . 130,269 +1,940  100.00% : 200 OK                          .  Ammo: urls.txt 
  99.5% <  15.0  15.0  12.0           .                                                           . Count: 138000
  99.0% <  12.0  12.0  11.3           . Net codes:                                                .  Load: line(300, 2000, 120s)
  95.0% <   5.6   6.2   7.3           . 130,269 +1,940  100.00% :  0 Success                      . 
  90.0% <   3.5   4.1   4.9           .                                                           . Active instances: 27
  85.0% <   2.3   2.9   3.9           . Average Sizes (all/last), bytes:                          . Planned requests: 1943.0 for 0:00:00
  80.0% <   1.8   2.2   3.2           .  Request:  55.1 /  55.1  ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇  . Actual responses: 1940
  75.0% <   1.6   1.8   2.4           . Response: 109.6 / 109.5  ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇  .         Accuracy: 0.00%
  70.0% <   1.5   1.6   2.0           .                                                           .         Time lag: 0:00:00
  60.0% <   1.3   1.4   1.6           . Average Times (all/last), ms:                             . 
  50.0% <   1.2   1.3   1.4           . Overall: 1.89 / 2.35  ▃▃▃▃▃▃▃▃▇▃▃▄▃▄▆▅▄▆▃▄▄▅▃▃▅▄▄▃▅▆▄▆▄▅  . 
  40.0% <   1.2   1.2   1.3           . Connect: 0.49 / 0.51  ▃▃▃▃▃▃▃▃▇▃▃▃▃▃▃▄▃▅▃▄▃▄▃▃▄▄▃▃▄▄▃▄▃▃  . 
  30.0% <   1.1   1.2   1.3           .    Send: 0.02 / 0.03  ▅▆▆▆▆▆▅▆▇▇▅▆▅▆▅▅▅▅▆▅▅▅▅▆▆▆▆▅▅▆▅▅▆▆  . 
  20.0% <   1.1   1.1   1.2           . Latency: 1.33 / 1.76  ▃▄▃▃▃▃▃▃▇▃▃▄▃▄▇▅▄▇▃▄▄▅▃▃▆▄▄▃▅▆▅▇▄▅  . 
  10.0% <   1.0   1.0   1.1           . Receive: 0.04 / 0.05  ▅▅▅▅▅▅▅▆▇▅▅▅▅▅▅▅▅▅▆▅▅▅▅▅▆▆▅▅▅▅▅▅▆▆  . 
                                                                                                  . 
                                                                                                  . 
 Cumulative Cases Info:                                                                           . 
     name   count       %   last net_e http_e avg ms last ms                                      . 
 OVERALL: 130,269 100.00% +1,940     0      0    1.9     2.4  ▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇  . 
```
