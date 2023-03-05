import numpy as np

def ema(arr, periods=14, weight=1, init=None):
    leading_na = np.where(~np.isnan(arr))[0][0]
    arr = arr[leading_na:]
    alpha = weight / (periods + (weight-1))
    alpha_rev = 1 - alpha
    n = arr.shape[0]
    pows = alpha_rev**(np.arange(n+1))
    out1 = np.array([])
    if 0 in pows:
        out1 = ema(arr[:int(len(arr)/2)], periods)
        arr = arr[int(len(arr)/2) - 1:]
        init = out1[-1]
        n = arr.shape[0]
        pows = alpha_rev**(np.arange(n+1))
    scale_arr = 1/pows[:-1]
    if init:
        offset = init * pows[1:]
    else:
        offset = arr[0]*pows[1:]
    pw0 = alpha*alpha_rev**(n-1)
    mult = arr*pw0*scale_arr
    cumsums = mult.cumsum()
    out = offset + cumsums*scale_arr[::-1]
    out = out[1:] if len(out1) > 0 else out
    out = np.concatenate([out1, out])
    out[:periods] = np.nan
    out = np.concatenate(([np.nan]*leading_na, out))
    return out


def atr(highs, lows, closes, periods=14, ema_weight=1):
    hi = np.array(highs)
    lo = np.array(lows)
    c = np.array(closes)
    tr = np.vstack([np.abs(hi[1:]-c[:-1]),
                    np.abs(lo[1:]-c[:-1]),
                    (hi-lo)[1:]]).max(axis=0)
    atr = ema(tr, periods=periods, weight=ema_weight)
    atr = np.concatenate([[np.nan], atr])
    return atr


def adx(highs, lows, closes, periods=14):
    highs = np.array(highs)
    lows = np.array(lows)
    closes = np.array(closes)
    up = highs[1:] - highs[:-1]
    down = lows[:-1] - lows[1:]
    up_idx = up > down
    down_idx = down > up
    updm = np.zeros(len(up))
    updm[up_idx] = up[up_idx]
    updm[updm < 0] = 0
    downdm = np.zeros(len(down))
    downdm[down_idx] = down[down_idx]
    downdm[downdm < 0] = 0
    _atr = atr(highs, lows, closes, periods)[1:]
    updi = 100 * ema(updm, periods) / _atr
    downdi = 100 * ema(downdm, periods) / _atr
    zeros = (updi + downdi == 0)
    downdi[zeros] = .0000001
    adx = 100 * np.abs(updi - downdi) / (updi + downdi)
    adx = ema(np.concatenate([[np.nan], adx]), periods)
    return adx

def adx_run(input_df, window_size=14):
    return adx(input_df['high'], input_df['low'], input_df['close'], periods=window_size)
