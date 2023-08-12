from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
import pywt
import tensorflow as tf
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense
from tensorflow.python.keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error

from utilities import plot_data


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
