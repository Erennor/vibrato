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
    return [i*100*127/sum for i in data]


def reduce_array(data):

    # return data
    new_data = [0]
    group_len = 16
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
            # group_len = #eventually update group_len
    if k == 0:
        new_data.pop(j)
    else:
        new_data[j] /= k
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
        ls['bary'] = []
    if len(ls['samples']) != len(ls['labels']):
        print("[WARN] erreur : database malforme")
    if 'samples' not in samples:
        samples['samples'] = []
        samples['labels'] = []
        samples['bary'] = {}
    if len(samples['samples']) != len(samples['labels']):
        print("[WARN] erreur : database malforme")
    mode = "deducting"
    label = "unitialized"

    lib = {"samples": ls["samples"] + samples["samples"],
        "labels": ls["labels"] + samples["labels"]}
    print lib["labels"]

    curr_data = []
    curr_barycentre = 0
    openHab = OpenHab()

    @staticmethod
    def calculate_barycentre(data):
        barycentre = 0
        weight = 0
        for i, elt in enumerate(data):
            barycentre += i*elt
            weight += elt
        return float(barycentre) / weight
    @staticmethod
    def parse(data):
        # eliminating la composante continue
        data = data[2:64]
        print data
        # eliminating imaginary values and taking absolute values
        data = [abs(elt) for i, elt in enumerate(data)]#if i % 2 == 0]
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
        Analyser.curr_barycentre += Analyser.calculate_barycentre(data)
        if len(Analyser.curr_data) <= 3:
            print "result added to array of hit"
        else:
            Analyser.mode = "deducting"
            Analyser.delete(Analyser.label)
            for data in Analyser.curr_data:
                Analyser.ls['samples'].append(data)
                Analyser.ls['labels'].append(Analyser.label)
                Analyser.ls['bary'][Analyser.label] = Analyser.curr_barycentre/4
            print "barycentre moyen = " + str(Analyser.curr_barycentre/4)
            Analyser.curr_data = []
            Analyser.curr_barycentre = 0
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
            clf = svm.SVC(kernel='poly',probability=True)
            if len(Analyser.ls['samples']) == 0:
                print("HitAnalyser : Aucune action faite car bibliotheque de coup vide")
                return "-1"
            if len(Analyser.lib["labels"]) <= 1:
                print "looool"
                return "-1"
            clf.fit(Analyser.lib['samples'], np.arange(len(Analyser.lib['labels'])))
            print "clf.predict_proba(data)"
            probas = clf.predict_proba(data)
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
        Analyser.curr_data = []
        Analyser.label = label
        Analyser.mode = "learning"

    @staticmethod
    def delete(label):
        Analyser.ls['samples'] = [data for i,data in enumerate(Analyser.ls['samples'])
                                  if Analyser.ls['labels'][i] !=label]
        Analyser.ls['labels'] = [elt for elt in Analyser.ls['labels'] if elt != label]
        Analyser.ls['bary'].pop(label)

    @staticmethod
    def change_adress(host, port):
        Analyser.openHab.openhab_port = port
        Analyser.openHab.openhab_host = host

    @staticmethod
    def cmd_handler(cmd):
        """Should handle cmd_label and d_label"""
        print("[DEBUG] : handle_cmd " + cmd)
        try:
            if cmd[0] == "d":
                Analyser.delete(cmd[2:])
            elif cmd[0] == "c":
                Analyser.set_learning(cmd[2:])
        except:
            print ("Error parsing command " + str(cmd))
        return


if __name__ == "__main__":
    print(Analyser.ls["labels"])
    print (Analyser.lib)
    Analyser.ls.close()