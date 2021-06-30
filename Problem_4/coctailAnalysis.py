from scipy.io import wavfile
import utilities as utl
import numpy as np
from FastICA import FastICA
import time

class AudioModel():
    def __init__(self, pathsList: list, sources: int):
        eps = 0.00000001
        rateList, dataList, shapeList, self.mixList, self.resultList = [], [], [], [], []
        for i in range(sources):
            if pathsList != None:
                rate, data = wavfile.read(pathsList[i])
                rateList.insert(i, rate)
                dataList.insert(i, data)
            else:
                pass
        for i in range(sources):
            shapeList.append(dataList[i].shape[0])
        minimum = min(shapeList)
        for i in range(sources):
            dataList[i] = dataList[i][0:minimum]
            # wavfile.write("result/coctailAnalysis/source#{}.wav".format(i+1), rateList[0], dataList[i])
        for i in range(sources):
            mixed = utl.mixSounds(dataList, self.generateWeights(sources)).astype(np.int16)
            self.mixList.insert(i, mixed)
            # wavfile.write("mixed{}.wav".format(i+1), rate, mixed)

        for i in range(sources):
            dataList[i] = dataList[i] - np.mean(dataList[i])
            dataList[i] = dataList[i]/32768
        matrix = np.vstack(dataList)
        whiteMatrix = utl.whitenMatrix(matrix)
        X = whiteMatrix
        vectors = []
        for i in range(0, X.shape[0]):
            vector = FastICA(X, vectors, eps)
            vectors.append(vector)
        W = np.vstack(vectors)
        S = np.dot(W, whiteMatrix)
        self.resultList = S
        # for i in range(sources):
            # wavfile.write("result/coctailAnalysis/ICAseparate#{}.wav".format(i), rateList[0], 5000*S[i].astype(np.int16))
        self.rate = rateList[0]
    def generateWeights(self, n):
        done = True
        while done:
            mixWeights = np.random.randint(100, size=n-1)
            mixWeights = np.append(mixWeights, 100 - np.sum(mixWeights))
            if np.sum(mixWeights) == 100 and mixWeights[n-1] > 0:
                done = False
        return mixWeights/100