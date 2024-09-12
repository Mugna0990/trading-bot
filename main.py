import trade_parameter as tp
import manager as mp
import config
import schedule
import time


phemex = config.define()


def bot():

    trend = mp.trend(phemex)  # determines LONG/SHORT
    open_price = mp.price(phemex)  # provide prices

    sig = trend.iloc[-1]['sig']
    open_size = float(tp.pos_size / 2)

    in_pos = mp.check_pnl(phemex)[1]  # checking if pnl has been reached

    if not in_pos:

        if sig == 'BUY':
            print("opening as a BUY")
            bp_1 = open_price.iloc[-1]['bp_1']
            bp_2 = open_price.iloc[-1]['bp_2']
            bp_1 = round(bp_1, 2)
            bp_2 = round(bp_2, 2)
            print(f'this is bp_1: {bp_1} this is bp_2: {bp_2}')

            phemex.cancel_all_orders(tp.pair)

            phemex.create_limit_buy_order(tp.pair, open_size, bp_1, tp.params)
            phemex.create_limit_buy_order(tp.pair, open_size, bp_2, tp.params)

            print('just make an order so going to sleep')
            time.sleep(120)
        elif sig == 'SELL':
            print("opening as a SELL")
            sp_1 = open_price.iloc[-1]['sp_1']
            sp_2 = open_price.iloc[-1]['sp_2']
            sp_1 = round(sp_1, 2)
            sp_2 = round(sp_2, 2)
            print(f'this is sp_1: {sp_1} this is sp_2: {sp_2}')

            phemex.cancel_all_orders(tp.pair)

            phemex.create_limit_sell_order(tp.pair, open_size, sp_1, tp.params)
            phemex.create_limit_sell_order(tp.pair, open_size, sp_1, tp.params)

            print('just make an order so going to sleep')
            time.sleep(120)
    else:
        print('already in position so not making new orders')


schedule.every(10).seconds.do(bot)

while True:
    try:
        schedule.run_pending()
    except:
        print('some issues are going on')
        time.sleep(30)
