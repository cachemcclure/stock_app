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
    def __init__(self):
        pass

    @abstractmethod
    def load_data(self, xx: np.array, yy: np.array):
        pass

    @abstractmethod
    def perform_analysis(self):
        pass

    @abstractmethod
    def plot_analysis(self):
        pass


class FastFourierTransform(BaseAnalysis):
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
