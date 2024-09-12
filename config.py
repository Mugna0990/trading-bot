import ccxt


def define():
    phemex = ccxt.phemex({
        'enableRateLimit': True,
        'apiKey': 'insert_your',
        'secret': 'insert_your',
    })
    return phemex
