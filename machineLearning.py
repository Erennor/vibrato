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
        if len(self.ls['samples']) == 1:
            return self.ls['labels'][0]
        if len(self.ls['samples']) == 0:
            print_debug("Aucune action faite car bibliotheque de coup vide")
            # todo : do nothing
            return 0
        return self.clf.predict(self.format(data).reshape(1, -1))[0]

    def __init__(self,ls):
        """Initialize shelves and algorithm"""
        self.ls = ls
        self.clf = svm.SVC(kernel='poly')
        if not self.ls.has_key('samples'):
            self.ls['samples'] = []
            self.ls['labels'] = []
        if not self.ls.has_key('links'):
            self.ls['links'] = dict()
        if len(self.ls['samples']) != len(self.ls['labels']):
            print_debug("erreur : database malforme")
        if len(self.ls['samples']) > 1:
            self.clf.fit(self.ls['samples'],self.ls['labels'])
        print('DEBUG: nb samples audio: ' + str(len(self.ls['samples'])))

    def learn(self, data, id):
        if id in self.ls['labels']:
            index = self.ls['labels'].index(id)
            self.ls['samples'][index] = self.format(data)
        else:
            self.ls['samples'].append(self.format(data))
            self.ls['labels'].append(id)
        if len(self.ls['samples']) > 1:
            self.clf.fit(self.ls['samples'],self.ls['labels'])








