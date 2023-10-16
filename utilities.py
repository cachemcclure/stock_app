from ratelimit import limits, sleep_and_retry
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import pywt


CALLS = 5
RATE_LIMIT = 61


@sleep_and_retry
@limits(calls=CALLS, period=RATE_LIMIT)
def check_limit():
    return


def log_handling(log_level: str = "ERROR", msg: str = "", log_file: str = "logs.txt"):
    out = f"{datetime.now()}: {log_level} - {msg}\n"
    with open(log_file, "a") as f:
        f.write(out)
    with open("master_logs.txt", "a") as f:
        f.write(out)


def plot_data(
    xx1: np.array,
    yy1: np.array,
    xx2: np.array = None,
    yy2: np.array = None,
    title: str = None,
    xlabel: str = None,
    ylabel: str = None,
):
    if (xx2 is None) and (yy2 is None):
        plt.plot(xx1, yy1)
    elif (xx2 is None) or (yy2 is None):
        raise Exception("ERROR: both xx2 AND yy2 must be provided if one is")
    else:
        plt.plot(xx1, yy1)
        plt.plot(xx2, yy2)
    if not (title is None):
        plt.title(title)
    if not (xlabel is None):
        plt.xlabel(xlabel)
    if not (ylabel is None):
        plt.ylabel(ylabel)
    plt.grid()
    plt.show()
    return


def low_pass_filter(signal, thresh=0.63, wavelet="db4"):
    thresh = thresh * np.nanmax(signal)
    coeff = pywt.wavedec(signal, wavelet, mode="per")
    coeff[1:] = (pywt.threshold(i, value=thresh, mode="soft") for i in coeff[1:])
    reconstructed_signal = pywt.waverec(coeff, wavelet, mode="per")
    return reconstructed_signal
