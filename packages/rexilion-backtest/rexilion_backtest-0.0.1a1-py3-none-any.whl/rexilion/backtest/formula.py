import numpy as np
import pandas as pd

def diff(arr):
    """
    Compute the first-order difference of an array using NumPy.
    Returns an array of the same length, with NaN in the first position.

    Parameters
    ----------
    arr : array-like
        Sequence of numeric values (e.g. a NumPy array or pandas Series).

    Returns
    -------
    numpy.ndarray
        First-difference array: diff[i] = arr[i] - arr[i-1], with diff[0] = NaN.
    """
    a = np.asarray(arr, dtype=float)
    diff = np.empty_like(a)
    diff[0] = np.nan
    diff[1:] = a[1:] - a[:-1]
    return diff

def rolling_sum(x, window):
    """
    Compute the rolling sum of a 1D array using NumPy.

    Parameters:
    x (numpy array): Input 1D array.
    window (int): Window size for the rolling sum.

    Returns:
    numpy array: Rolling sum array.
    """
    # Create a cumulative sum array
    cumsum = np.cumsum(x)
    
    # Compute the rolling sum using the cumulative sum
    rolling_sum = cumsum[window - 1:] - np.concatenate(([0], cumsum[:-window]))
    
    # Pad the result with NaN or zeros to match the original array length
    rolling_sum = np.concatenate(([np.nan] * (window - 1), rolling_sum))
    
    return rolling_sum

def rolling_mean(array, rolling_window):
    array = np.nan_to_num(array, nan=0)  # Replace NaNs with zero
    if rolling_window > len(array):
        return np.full_like(array, np.nan)

    cumsum = np.zeros(len(array) + 1)
    cumsum[1:] = np.cumsum(array)  # Avoid inserting 0 manually
    rolling_sum = cumsum[rolling_window:] - cumsum[:-rolling_window]
    rolling_mean = rolling_sum / rolling_window

    # Prepend NaNs for first (window - 1) values
    rolling_mean = np.concatenate((np.full(rolling_window - 1, np.nan), rolling_mean))
    return rolling_mean

def rolling_ema(data, window):
    if window > len(data):
        return np.full_like(data, np.nan)

    multiplier = 2 / (window + 1)
    ema_values = np.zeros_like(data, dtype=np.float64)

    # Compute the initial SMA for first 'window' values
    ema_values[window - 1] = np.mean(data[:window])

    # Compute the EMA for remaining values
    for i in range(window, len(data)):
        ema_values[i] = (data[i] - ema_values[i - 1]) * multiplier + ema_values[i - 1]

    # Set first `window-1` values to NaN since they can't be computed
    ema_values[:window - 1] = np.nan
    return ema_values

def rolling_wma(data, window):
    if window > len(data):
        return np.full_like(data, np.nan)

    weights = np.arange(1, window + 1)
    wma = np.convolve(data, weights[::-1], mode='valid') / weights.sum()

    # Pad with NaN to match original array length
    wma = np.concatenate((np.full(window - 1, np.nan), wma))
    return wma

def rolling_std(array, rolling_window):
    array = np.nan_to_num(array, nan=0)  # Replace NaNs with zero
    if rolling_window > len(array):
        return np.full_like(array, np.nan)

    # Calculate the rolling mean
    cumsum = np.zeros(len(array) + 1)
    cumsum[1:] = np.cumsum(array)
    rolling_sum = cumsum[rolling_window:] - cumsum[:-rolling_window]
    rolling_mean = rolling_sum / rolling_window

    # Calculate the rolling variance
    cumsum_sq = np.zeros(len(array) + 1)
    cumsum_sq[1:] = np.cumsum(array**2)
    rolling_sum_sq = cumsum_sq[rolling_window:] - cumsum_sq[:-rolling_window]
    rolling_variance = (rolling_sum_sq - rolling_sum * rolling_mean) / rolling_window

    # Ensure variance is non-negative (clip to zero)
    rolling_variance = np.clip(rolling_variance, 0, None)

    # Calculate the rolling standard deviation
    rolling_std = np.sqrt(rolling_variance)

    # Prepend NaNs for first (window - 1) values
    rolling_std = np.concatenate((np.full(rolling_window - 1, np.nan), rolling_std))
    return rolling_std

def rolling_min(array, rolling_window):
    return pd.Series(array).rolling(rolling_window).min().to_numpy()

def rolling_max(array, rolling_window):
    return pd.Series(array).rolling(rolling_window).max().to_numpy()

def rolling_mean_normalize(array, rolling_window):
    sma = rolling_mean(array, rolling_window)
    min_val = rolling_min(array, rolling_window)
    max_val = rolling_max(array, rolling_window)
    return (array - sma) / (max_val - min_val + 1e-9)

def rolling_zscore_mean(array, rolling_window):
    sma = rolling_mean(array, rolling_window)
    stddev = rolling_std(array, rolling_window)
    zscore = (array - sma) / stddev
    return zscore - rolling_mean(zscore, rolling_window)

def rolling_sigmoid_zscore(array, rolling_window):
    sma = rolling_mean(array, rolling_window)
    stddev = rolling_std(array, rolling_window)
    return 2 * (1 / (1 + np.exp(-(array - sma) / stddev))) - 1

def rolling_minmax_normalize(array, rolling_window):
    min_val = rolling_min(array, rolling_window)
    max_val = rolling_max(array, rolling_window)
    return 2 * (array - min_val) / (max_val - min_val + 1e-9) - 1

def rolling_skew(arr, window):
    n = arr.shape[0]
    if n < window:
        return np.full(n, np.nan)  # Return all NaNs if not enough data

    rolling_skew = np.full(n, np.nan)  # Full-length array, pre-filled with NaNs

    for i in range(n - window + 1):
        window_data = arr[i:i + window]  # Extract rolling window
        mean = np.mean(window_data)
        std = np.std(window_data, ddof=1)  # Sample std (ddof=1)
        
        if std != 0:  # Avoid division by zero
            rolling_skew[i + window - 1] = (window / ((window - 1) * (window - 2))) * np.sum(
                ((window_data - mean) / std) ** 3
            )

    return rolling_skew

def rolling_var(arr, window):
    n = arr.shape[0]
    if n < window:
        return np.full(n, np.nan)

    rolling_var = np.full(n, np.nan)

    for i in range(n - window + 1):
        window_data = arr[i:i + window]
        rolling_var[i + window - 1] = np.var(window_data, ddof=1)  # Sample variance

    return rolling_var

def rolling_kurt(arr, window):
    n = arr.shape[0]
    if n < window:
        return np.full(n, np.nan)

    rolling_kurt = np.full(n, np.nan)

    for i in range(n - window + 1):
        window_data = arr[i:i + window]
        mean = np.mean(window_data)
        std = np.std(window_data, ddof=1)

        if std != 0:
            m4 = np.mean(((window_data - mean) / std) ** 4)
            # Excess kurtosis: subtract 3 (optional, comment out if you want regular kurtosis)
            rolling_kurt[i + window - 1] = m4 - 3

    return rolling_kurt

def rolling_zscore(array, rolling_window):
    """
    Returns a NumPy array of rolling z-scores with a window of `rolling_window`.
    The first rolling_window-1 entries will be NaN.
    """
    sma    = rolling_mean(array, rolling_window)
    stddev = rolling_std(array, rolling_window)
    # plain z-score:
    return (array - sma) / stddev

def rolling_tanh_estimator(arr, rolling_window):
    sma    = rolling_mean(arr, rolling_window)
    stddev = rolling_std(arr, rolling_window)
    return np.tanh(0.01 * (arr - sma) / (stddev + 1e-9))

def sigmoid(arr):
    return 2 * (1 / (1 + np.exp(arr))) - 1

def rolling_softmax(arr, rolling_window):
    n = len(arr)
    softmax = np.full(n, np.nan)
    for i in range(rolling_window - 1, n):
        window = arr[i - rolling_window + 1:i + 1]
        exps = np.exp(window - np.max(window))
        softmax[i] = 2 * (exps[-1] / np.sum(exps)) - 1
    return softmax

def rolling_l1_normalization(arr, rolling_window):
    abs_sum = rolling_sum(np.abs(arr), rolling_window)
    return 2 * (arr / (abs_sum + 1e-9)) - 1

def rolling_rsi(df, rolling_window):
    def calculate_rsi(series):
        delta = series.diff()
        gain = rolling_mean(delta.where(delta > 0, 0), rolling_window)
        loss = rolling_mean(-delta.where(delta < 0, 0), rolling_window)
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    df["rsi"] = calculate_rsi(df["data"])
    df["sma"] = rolling_mean(df["rsi"], rolling_window)
    df["ema"] = rolling_ema(df["rsi"], rolling_window)
    df["wma"] = rolling_wma(df["rsi"], rolling_window)
    df["processed_data"] = (df["rsi"] - 50) / 50 
    return df

def rolling_bollinger_bands(df, rolling_window, multiplier):
    df["sma"] = rolling_mean(df["data"], rolling_window)
    df["ema"] = rolling_ema(df["data"], rolling_window)
    df["wma"] = rolling_wma(df["data"], rolling_window)
    df["upper_band"] = df["sma"] + (multiplier * rolling_std(df["data"], rolling_window))
    df["lower_band"] = df["sma"] - (multiplier * rolling_std(df["data"], rolling_window))
    return df

def calculate_macd(df, short_window, long_window, signal_window=9):
    # Calculate the short-term and long-term EMA
    df["EMA_short"] = rolling_ema(df["data"], short_window)
    df["EMA_long"] = rolling_ema(df["data"], long_window)
    # Calculate MACD line
    df["MACD"] = df["EMA_short"] - df["EMA_long"]
    # Calculate Signal line
    df["Signal"] = rolling_ema(df["MACD"], signal_window)
    # Calculate Histogram
    df["Histogram"] = df["MACD"] - df["Signal"]
    return df