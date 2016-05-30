from sklearn import svm
import shelve
import numpy as np
import signal
import sys
from debug import print_debug


class MachineLearning:
    def format(self, datas):
        res = np.arange(0, len(datas)*datas[0].shape[0])
        for i in range(0, len(datas)):
            for j in range(0, datas[0].shape[0]):
                res[i*datas[0].shape[0] + j] = datas[i][j]
        return res

    def guessing(self, data):
        """
        from one hit data, return the label of the most look-alike hit from the database
        """            
        if len(self.ls['samples']) > 1:
            self.clf.fit(self.ls['samples'],np.arange(len(self.ls['labels'])))
        if len(self.ls['samples']) == 1:
            return self.ls['labels'][0]
        if len(self.ls['samples']) == 0:
            print_debug("Aucune action faite car bibliotheque de coup vide")
            return "-1"
        return self.ls['labels'][self.clf.predict(self.format(data).reshape(1, -1))[0]]

    def __init__(self,ls):
        """Initialize shelves and algorithm"""
        self.ls = ls
        self.clf = svm.SVC(kernel='poly')
        if not self.ls.has_key('samples'):
            self.ls['samples'] = []
            self.ls['labels'] = []
        if len(self.ls['samples']) != len(self.ls['labels']):
            print_debug("erreur : database malforme")
        if len(self.ls['samples']) > 1:
            self.clf.fit(self.ls['samples'],np.arange(len(self.ls['labels'])))

    def learn(self, data, hitId):
        """
            associate id to sample data in the database
        """
        if hitId in self.ls['labels']:
            index = self.ls['labels'].index(hitId)
            self.ls['samples'][index] = self.format(data)
        else:
            self.ls['samples'].append(self.format(data))
            self.ls['labels'].append(hitId)








