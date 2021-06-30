import numpy as np
import pandas as pd
from sklearn.decomposition import FastICA
from scipy import signal

class SignalModel():
    def __init__(self, signalPath: str):
        s0 = pd.read_csv(signalPath)
        n_samples = s0.shape[0]
        time = np.linspace(0, s0.shape[0], n_samples)
        s1 = signal.sawtooth(50 * np.pi * time)
        self.temp  = s1
        S = np.c_[s0, s1]
        S /= S.std(axis=0)

        A = np.array([[1, 1, 1], [0.5, 2, 1.0], [1.5, 1.0, 2.0]])
        self.mix = np.dot(S, A.T)

        ica = FastICA(n_components=2)
        self.separate = ica.fit_transform(self.mix)