import shelve
from sklearn import svm
import numpy as np
from openhab import OpenHab


class Analyser:
    """ supposed to choose what to do from hearing a hit"""
    biblio = "new_sample.db"
    ls = shelve.open(biblio, writeback=True)
    if not ls.has_key('samples'):
        ls['samples'] = []
        ls['labels'] = []
    if len(ls['samples']) != len(ls['labels']):
        print("[WARN] erreur : database malforme")
    mode = "learning"
    label = "sample2"
    openhab = OpenHab()
    i = 0

    @staticmethod
    def format(datas):
        res = np.arange(0, len(datas) * datas[0].shape[0])
        for i in range(0, len(datas)):
            for j in range(0, datas[0].shape[0]):
                res[i * datas[0].shape[0] + j] = datas[i][j]
        return res

    @staticmethod
    def learn(data):
        if Analyser.label in Analyser.ls['labels']:
            index = Analyser.ls['labels'].index(Analyser.label)
            Analyser.ls['samples'][index] = data
        else:
            Analyser.ls['samples'].append(data)
            Analyser.ls['labels'].append(Analyser.label)

    @staticmethod
    def analyse(data):
        if Analyser.mode == "learning":
            print "learning"
            Analyser.label = "sample" + str(Analyser.i)
            Analyser.i += 1
            Analyser.learn(data)
            Analyser.mode = "learning"
            return 0
        else:
            clf = svm.SVC(kernel='poly')
            if len(Analyser.ls['samples']) > 1:
                clf.fit(Analyser.ls['samples'], np.arange(len(Analyser.ls['labels'])))
            if len(Analyser.ls['samples']) == 1:
                return Analyser.ls['labels'][0]
            if len(Analyser.ls['samples']) == 0:
                print("HitAnalyser : Aucune action faite car bibliotheque de coup vide")
                return "-1"
            res = Analyser.ls['labels'][clf.predict(data)[0]]
            Analyser.openhab.post_command("scriptListener", res)
            return res

    @staticmethod
    def set_learning(label):
        Analyser.label = label
        Analyser.mode = "learning"

    @staticmethod
    def delete(label):
        try:
            index = Analyser.ls['labels'].index(label)
            Analyser.ls['samples'].pop(index)
            Analyser.ls['labels'].pop(index)
        except:
            print("Error, label not present in database")

    @staticmethod
    def change_adress(host, port):
        Analyser.openhab.openhab_port = port
        Analyser.openhab.openhab_host = host

    @staticmethod
    def cmd_handler(cmd):
        """Should handle cmd_label and d_label"""
        print("[DEBUG] : handle_cmd " + cmd)
        try:
            if cmd[0] == "d":
                Analyser.delete(cmd[2:])
            elif cmd[0] == "c":
                Analyser.mode = "learning"
                Analyser.label = cmd[2:]
        except:
            print ("Error parsing command " + str(cmd))
        return

if __name__ == "__main__":
    print(Analyser.ls)
    Analyser.ls.close()