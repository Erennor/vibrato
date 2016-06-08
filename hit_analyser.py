import shelve
from sklearn import svm
import numpy as np
from openhab import OpenHab





class Analyser:
    """ supposed to choose what to do from hearing a hit"""
    biblio = "new_sample.db"
    ls = shelve.open(biblio, writeback=True)
    samples = shelve.open("samples.db", writeback=False)
    if not ls.has_key('samples'):
        ls['samples'] = []
        ls['labels'] = []
    if len(ls['samples']) != len(ls['labels']):
        print("[WARN] erreur : database malforme")
    mode = "deducting"
    label = "unitialized"
    # todo : assert no values from ls belongs to samples
    lib = {"samples": ls["samples"] + samples["samples"],
           "labels": ls["labels"] + samples["labels"]}
    print lib["labels"]

    openhab = OpenHab()

    @staticmethod
    def parse(data):
        print "DATAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA, tu fais chier robichou"
        print data
        return data

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
        Analyser.lib = {"samples": Analyser.ls["samples"] + Analyser.samples["samples"],
                        "labels": Analyser.ls["labels"] + Analyser.samples["labels"]}
        print Analyser.lib["labels"]

    @staticmethod
    def analyse(data):
        data = Analyser.parse(data)
        if Analyser.mode == "learning":
            Analyser.learn(data)
            Analyser.mode = "deducting"
            return 0
        else:
            clf = svm.SVC(kernel='poly', probability=True)
            if len(Analyser.ls['samples']) == 0:
                print("HitAnalyser : Aucune action faite car bibliotheque de coup vide")
                return "-1"
            clf.fit(Analyser.lib['samples'], np.arange(len(Analyser.lib['labels'])))
            print "clf.predict_proba(data)"
            probas = clf.predict_proba(data)
            print "probas = " + str(probas)
            int_res = clf.predict(data)[0]
            print "int_res = " + str(int_res)
            res = Analyser.lib['labels'][int_res]
            print res
            if res in Analyser.ls['labels']:
                print "best candidate is a registered hit"
                print probas[0][int_res]
                if probas[0][int_res] > 0.5:
                    print "probability over 50% : proceeding"
                    Analyser.openhab.post_command("scriptListener", res)
                    return res
            return 0

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