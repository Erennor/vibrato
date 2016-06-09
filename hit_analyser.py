import shelve
from sklearn import svm
import numpy as np
from openhab import OpenHab



def print_data(data):
    for i in data:
        line = ""
        for j in np.arange(i/20):
            line += "#"
        print line

def normalize_array(data):
    sum = 0
    for i in data:
        sum += i
    moy = sum / 126
    mult = 100 / moy
    return [i*mult for i in data]


def reduce_array(data):
    new_data = [0]
    group_len = len(data)/16
    j = 0
    k = 0
    for i in data:
        new_data[j] += i
        k += 1
        if k == group_len:
            new_data[j] = int( new_data[j]/group_len)
            new_data.append(0)
            k = 0
            j += 1
    int(new_data[j] / (k + 1))
    print new_data
    return new_data


class Analyser:
    """ supposed to choose what to do from hearing a hit"""
    sample_learning = 3
    biblio = "new_sample.db"
    ls = shelve.open(biblio, writeback=True)
    samples = shelve.open("samples.db", writeback=False)
    if not ls.has_key('samples'):
        ls['samples'] = []
        ls['labels'] = []
    if len(ls['samples']) != len(ls['labels']):
        print("[WARN] erreur : database malforme")
    if 'samples' not in samples:
        samples['samples'] = []
        samples['labels'] = []
    if len(samples['samples']) != len(samples['labels']):
        print("[WARN] erreur : database malforme")
    mode = "deducting"
    label = "unitialized"

    lib = {"samples": ls["samples"] + samples["samples"],
        "labels": ls["labels"] + samples["labels"]}
    print lib["labels"]

    curr_data = []
    openhab = OpenHab()

    @staticmethod
    def parse(data):
        real_data = []
        for i in np.arange(len(data)):
            if i % 2 == 0:
                real_data.append(data[i])
        data = normalize_array(real_data)
        data = reduce_array(data)
        print_data(data)
        barycentre = 0
        weight = 0
        for i, elt in enumerate(data):
            barycentre += i*elt
            weight += elt
        barycentre /= weight
        print "Barycentre : " + str(barycentre)
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
        Analyser.curr_data.append(data)
        if len(Analyser.curr_data) <= 3:
            return
        data = [0] * len(data)
        for i in np.arange(len(data)):
            for sample in Analyser.curr_data:
                data[i] += sample[i]/3
        print_data(data)
        Analyser.curr_data = []
        Analyser.mode = "deducting"
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
            return 0
        else:
            clf = svm.SVC(kernel='poly')
            if len(Analyser.ls['samples']) == 0:
                print("HitAnalyser : Aucune action faite car bibliotheque de coup vide")
                return "-1"
            if len(Analyser.lib["labels"]) <= 1:
                print "looool"
                return "-1"
            clf.fit(Analyser.lib['samples'], np.arange(len(Analyser.lib['labels'])))
            print "clf.predict_proba(data)"
            probas = clf.decision_function(data)
            print "probas = " + str(probas)
            int_res = clf.predict(data)[0]
            print
            print "int_res = " + str(int_res)
            res = Analyser.lib['labels'][int_res]
            print res
            if res in Analyser.ls['labels']:
                print "best candidate is a registered hit"
                print probas #[0][int_res]
                #if probas[0][int_res] > 0.5:
                 #   print "probability over 50% : proceeding"
                  #  Analyser.openhab.post_command("scriptListener", res)
                   # return res
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
    print(Analyser.ls["labels"])
    print (Analyser.lib)
    Analyser.ls.close()