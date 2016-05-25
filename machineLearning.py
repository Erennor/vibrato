from sklearn import svm
import shelve
import numpy as np
import signal
import sys


biblio = 'new_sample.db'
ls = shelve.open(biblio, writeback=True)

class MachineLearning:
    def format(self, datas):
        res = np.arange(0, len(datas)*datas[0].shape[0])
        for i in range(0, len(datas)):
            for j in range(0, datas[0].shape[0]):
                res[i*datas[0].shape[0] + j] = datas[i][j]
        return res

    def guessing(self, data):
        return self.clf.predict(self.format(data).reshape(1, -1))

    def guessingInit(self):
        ###init the algorithm
        self.clf = svm.SVC(kernel='poly')

        ###download the samples and give them to the algorithm
        global ls
        # fetching samples sizes
        self.microSampleIndex = ls['META'][0]
        self.arduinoSampleIndex = ls['META'][1]
        samplesList = []
        if self.microInput:
            resultsArray = np.arange(0, self.microSampleIndex)
            for i in range(0, self.microSampleIndex):
                print("[DEBUG] GuessingInit  loop i=" + str(i) + "/" + str(self.microSampleIndex))
                samplesList.append(ls["micro" + str(i)][0])
                resultsArray[i] = ls["micro" + str(i)][1]
        else:
            resultsArray = np.arange(0, self.arduinoSampleIndex)
            for i in range(0, self.arduinoSampleIndex):
                samplesList.append(ls["arduino" + str(i)][0])
                resultsArray[i] = ls["arduino" + str(i)][1]
        samplesArray = np.array(samplesList)
        self.clf.fit(samplesArray, resultsArray)

    def __init__(self, microInput):
        global ls
        #A modifier
        self.microInput = microInput
        if not ls.has_key('META'):
            ls['META'] = [0, 0]
        self.microSampleIndex = ls['META'][0]
        self.arduinoSampleIndex = ls['META'][1]
        print('DEBUG: nb samples audio: ' + str(self.microSampleIndex))

    def learn(self, data, result):
        resultArray = np.arange(1)
        resultArray[0] = result
        global ls
        if self.microInput:
            ls["micro"+str(self.microSampleIndex)] = [self.format(data), resultArray]
            self.microSampleIndex += 1
            ls['META'][0] = self.microSampleIndex
        else:
            ls["arduino"+str(self.arduinoSampleIndex)] = [self.format(data), resultArray]
            self.arduinoSampleIndex += 1
            ls['META'][1] = self.arduinoSampleIndex







