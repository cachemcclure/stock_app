from abc import ABC
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
import pywt
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error


class BaseAnalysis(ABC):
    pass


class FastFourierTransform(BaseAnalysis):
    pass


class DiscreteWaveletTransform(BaseAnalysis):
    pass


class DiscreteWaveletPacketTransform(BaseAnalysis):
    pass
