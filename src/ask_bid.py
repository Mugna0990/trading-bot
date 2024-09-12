import trade_parameter as tp


def ask(phemex):
    ob = phemex.fetch_order_book(tp.pair)
    asks = ob['asks'][0][0]
    return asks


def bid(phemex):
    ob = phemex.fetch_order_book(tp.pair)
    bids = ob['bids'][0][0]
    return bids
