import trade_parameter as tp
import ask_bid
import time
import sma


def trend(phemex):

    # if bid < the 20 day sma = BEARISH => SELL
    # if bid > 20 day sma = BULLISH => BUY

    bid = ask_bid.ask(phemex)
    df_d = sma.daily_sma(phemex)

    df_d['sig'] = 'NULL'
    df_d.loc[df_d['sma20_d'] > bid, 'sig'] = 'SELL'
    df_d.loc[df_d['sma20_d'] < bid, 'sig'] = 'BUY'

    return df_d


def price(phemex):

    df_f = sma.fifteen_sma(phemex)

    df_f['bp_1'] = df_f['sma20_15'] * 1.001  # 15m sma .1% above
    df_f['bp_2'] = df_f['sma20_15'] * .997  # 15m sma .3% below
    df_f['sp_1'] = df_f['sma20_15'] * .999  # 15m sma .1% below
    df_f['sp_2'] = df_f['sma20_15'] * 1.003  # 15m sma .3% over

    return df_f



def open_position(phemex):   # data collection about open positions

    params = {'type': 'swap', 'code': 'USD'}
    balance = phemex.fetch_balance(params=params)
    open_pos = balance['info']['data']['positions']
    open_bool = False
    long = None

    side = open_pos[0]['side']
    size = open_pos[0]['size']

    if side == 'Buy':
        open_bool = True
        long = True
    elif side == 'Sell':
        open_bool = True
        long = False

    return open_pos, open_bool, size, long


def kill_switch(phemex):

    # limit close order
    openpos = open_position(phemex)[1]

    while openpos:      # repeat until there are open positions

        print('starting kill switch')

        phemex.cancel_all_orders(tp.pair)

        long = open_position(phemex)[3]
        kill_size = int(open_position(phemex)[2])

        if not long:

            bid = ask_bid.bid(phemex)

            phemex.create_limit_buy_order(tp.pair, kill_size, bid, tp.params)
            print(f'made a BUY to CLOSE of {kill_size}{tp.pair} at {bid}$')
            time.sleep(30)

        elif long:

            ask = ask_bid.ask(phemex)

            phemex.create_limit_sell_order(tp.pair, kill_size, ask, tp.params)
            print(f'made a SELL to CLOSE of {kill_size}{tp.pair} at {ask}$')
            time.sleep(30)

        else:
            print('something wrong happened')

        openpos = open_position(phemex)[1]


def check_pnl(phemex):

    print('checking to see if it is time to exit')

    params = {'type': "swap", 'code': 'USDT'}
    pos_dict = phemex.fetch_positions(params=params)

    pos_dict = pos_dict[0]
    side = pos_dict['info']['side']
    size = pos_dict['info']['size']
    leverage = float(pos_dict['info']['size'])
    entry = float(pos_dict['entryPrice'])

    current_price = ask_bid.bid(phemex)
    perc = 0
    long = None
    check_order = False

    if entry != 0:
        if side == 'Buy':
            diff = current_price - entry
            long = True
        else:
            diff = entry - current_price
            long = False
        perc = round((diff / entry) * leverage, 10)
        check_order = True

    perc = 100*perc
    print(f'this is PNL percentage: {perc} %')

    pnlclose = False
    if check_order:

        in_pos = True
        print('in position')

        if perc >= tp.target:
            print('target hitted')
            pnlclose = True
            kill_switch(phemex)
            time.sleep(600)

        elif perc < 0:
            print('losing position')
            if perc <= tp.stop_loss:
                print('starting stop-loss process')
                pnlclose = True
                kill_switch(phemex)
        else:
            print('target not hit yet')

    else:
        in_pos = False
        print('not in position')

    print('finished PNL checking')

    return pnlclose, in_pos, size, long
