from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
import pywt
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error

from utilities import plot_data, low_pass_filter


class BaseAnalysis(ABC):
    @abstractmethod
    def __init__(self, **kwargs):
        pass

    @abstractmethod
    def perform_analysis(self, **kwargs):
        pass

    @abstractmethod
    def plot_analysis(self, **kwargs):
        pass

    @abstractmethod
    def extrapolate_points(self, **kwargs):
        pass

    @abstractmethod
    def plot_extrapolation(self, **kwargs):
        pass

    @abstractmethod
    def filter_data(self, **kwargs):
        pass


class FastFourierTransform(BaseAnalysis):
    def __init__(self):
        super().__init__()
        return

    def perform_analysis(
        self, xx: np.array, yy: np.array, sample_points: int, sample_spacing: int
    ):
        yf = np.fft.fft(xx)
        xf = np.fft.fftfreq(sample_points, sample_spacing)[: sample_points // 2]
        return xf, yf

    def plot_analysis(
        self,
        source_data_xx: np.array,
        source_data_yy: np.array,
        analyzed_data_xx: np.array,
        analyzed_data_yy: np.array,
    ):
        plot_data(
            xx1=source_data_xx,
            yy1=source_data_yy,
            xx2=analyzed_data_xx,
            yy2=analyzed_data_yy,
            title="FFT Analysis",
            xlabel="Date",
            ylabel="Stock Price",
        )
        return

    def extrapolate_points(self, xx: np.array, n_predict: int):
        nn = xx.size
        n_harm = 10  # number of harmonics in model
        tt = np.arange(0, nn)
        pp = np.polyfit(tt, xx, 1)  # find linear trend in x
        x_notrend = xx - pp[0] * tt  # detrended x
        x_freqdom = np.fft.fft(x_notrend)  # detrended x in frequency domain
        f = np.fft.fftfreq(nn)  # frequencies
        indexes = range(nn)
        # sort indexes by frequency, lower -> higher
        indexes.sort(key=lambda ii: np.absolute(f[ii]))

        tt = np.arange(0, nn + n_predict)
        restored_sig = np.zeros(tt.size)
        for ii in indexes[: 1 + n_harm * 2]:
            ampli = np.absolute(x_freqdom[ii]) / nn  # amplitude
            phase = np.angle(x_freqdom[ii])  # phase
            restored_sig += ampli * np.cos(2 * np.pi * f[ii] * tt + phase)
        return restored_sig + pp[0] * tt

    def plot_extrapolation(self, **kwargs):
        return

    def filter_data(self, ts_signal, threshold):
        return


class SignalFiltering(BaseAnalysis):
    def __init__(self):
        super().__init__()
        return

    def load_data(self, xx: np.array, yy: np.array):
        return

    def perform_analysis(self):
        return

    def plot_analysis(self):
        return

    def filter_data(self, ts_signal, threshold):
        return


class DiscreteWaveletTransform(BaseAnalysis):
    def __init__(self):
        super().__init__()
        return

    def load_data(self, xx: np.array, yy: np.array):
        return

    def perform_analysis(self):
        return

    def plot_analysis(self):
        return

    def filter_data(self, ts_signal, threshold):
        return


class DiscreteWaveletPacketTransform(BaseAnalysis):
    def __init__(self):
        super().__init__()
        return

    def load_data(self, xx: np.array, yy: np.array):
        return

    def perform_analysis(self):
        return

    def plot_analysis(self):
        return

    def filter_data(self, ts_signal, threshold):
        return
