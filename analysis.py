from abc import ABC


class BaseAnalysis(ABC):
    pass


class FastFourierTransform(BaseAnalysis):
    pass


class DiscreteWaveletTransform(BaseAnalysis):
    pass


class DiscreteWaveletPacketTransform(BaseAnalysis):
    pass
