import pandas as pd
import trade_parameter as tp


def fifteen_sma(phemex):
    print('starting indis 15m...')

    timeframe = '15m'
    num_bars = 100

    bars = phemex.fetch_ohlcv(tp.pair, timeframe=timeframe, limit=num_bars)
    df_f = pd.DataFrame(bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df_f['timestamp'] = pd.to_datetime(df_f['timestamp'], unit='ms')

    # 15min SMA - 20 day
    df_f['sma20_15'] = df_f.close.rolling(20).mean()
    df_f.dropna(inplace=True)

    return df_f


def daily_sma(phemex):
    print('starting indis 1d...')

    timeframe = '1d'
    num_bars = 100

    bars = phemex.fetch_ohlcv(tp.pair, timeframe=timeframe, limit=num_bars)
    df_d = pd.DataFrame(bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df_d['timestamp'] = pd.to_datetime(df_d['timestamp'], unit='ms')

    # DAILY SMA - 20 day
    df_d['sma20_d'] = df_d.close.rolling(20).mean()
    df_d.dropna(inplace=True)

    return df_d
