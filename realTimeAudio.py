import ui_plot
import sys
import signal
import threading
import numpy as np
from scipy import stats
from PyQt4 import QtCore, QtGui
import PyQt4.Qwt5 as Qwt
from recorder import *
import peak_detect as peak
import os
from math import *
from machineLearning import *
from arduinoReader import *
from tcp_listener import *
from hit_handler import *
from debug import *

""" perpetually running program, intercept openHab command via listener and has access to 
    """
def plotSomething():
    global microInput
    global curWait
    global learn
    global result
    global ml
    global absCpt
    global newOpenHabAction
    global it_light
    global it_rollershutter
    global it_up
    global it_down
    global ct
    global datas
    global tempOpenHabAction
    global tmpAction
    global inWaintingOHA
    global listener
    global handler
    # Handle openHab listener
    # treat possible commands
    if listener.hasCommand:
        print_debug("listener has command")
        handler.openHab.post_command("Waiting","OFF")
        handler.handle_cmd(listener.availableData)
        listener.availableData = ""
        listener.hasCommand = False
    # newInput define if new datas are avaible
    if microInput:
        newInput = SR.newAudio
    else:
        newInput = AR.newArduino

    if newInput == False:
        return
    # get datas
    if microInput:
        xs, ys = SR.fft()
    else:
        global xAr
        xs = xAr
        ys = AR.getArduino()

    c.setData(xs, ys)
    uiplot.qwtPlot.replot()

    # peak detection 
    _max, _min = peak.peakdetect(ys, xs, 30, 0.30)

    slope, intercept, r_value, p_value, std_err = stats.linregress(xs, ys)
    THRESHOLD = 10000
    thresholdIsReached = ys > THRESHOLD
    thresholdIsReached[1:][thresholdIsReached[:-1] & thresholdIsReached[1:]] = False
    iterateur = 1
    if thresholdIsReached.any():
        pass
        # print_debug("Lin Reg: " + str(slope) + "Peaks detected: " + str(_max))
    # end peak detection

    # signal analysis 
    curMean = np.mean(ys)

    if inWaintingOHA and ct > 30:
        newOpenHabAction = True
        inWaintingOHA = False
        openHabAction = np.arange(1)
        openHabAction[0] = tmpAction
        ct = 0

    # signal intensity reached some level defined by HITLIMIT
    if (curMean > HITLIMIT or curWait > 0) and ct > BEGINCOUNT:
        if ct < 20:
            tempOpenHabAction = True
        if curWait < WAITLIMIT:
            datas.append(ys)
            # print('on a rentre 1 data')
            curWait += 1
        else:
            if handler.learn:
                ml.learn(datas,handler.recordLabel)
                print_debug("coup " + str(absCpt) + " enregistre sous l'identifiant " + handler.recordLabel)
                handler.learn = False
                handler.openHab.post_command("WaitCreate","OFF")
            else:
                hitId = ml.guessing(datas)
                if(hitId != "-1"):
                    handler.handle_hit(hitId)
            curWait = 0
            ct = 0
            datas = []
    else:
        ct += 1
    absCpt += 1
    if microInput:
        SR.newAudio = False
    else:
        AR.newArduino = False

def close_all():
    handler.openHab.post_command("Waiting","ON")

    try:
        print_debug("trying to close connection")
        Listener.my_connection.close()
        print_debug("Connection closed")
    except:
        pass
    finally:
        ls.close()
        print_debug("Shelves closed")
        win_plot.close()
        app.quit()
        print_debug("Qt application closed")

def signal_handler(signal,frame):
    print_debug("Signal " + str(signal) + " received on frame " + str(frame))
    close_all()


signal.signal(signal.SIGINT, signal_handler)

if __name__ == "__main__":
    print_debug("debug main, go to print_debug.py to change display")
    microInput = True
    procede = False
    learn = False
    biblio = 'new_sample.db'
    ls = shelve.open(biblio, writeback=True)
    global newOpenHabAction
    newOpenHabAction = False
    global tempOpenHabAction
    tempOpenHabAction = False
    global inWaintingOHA
    inWaintingOHA = False
    global it_rollershutter
    it_rollershutter = 1
    global it_light
    it_light = 1
    global it_up
    it_up = 1
    global it_down
    it_down = 1
    global absCpt
    absCpt = 0
    global ct
    ct = 0
    global datas
    datas = []
    listener = Listener()
    listener.start_listening()
    handler = Handler(microInput,ls)
    handler.openHab.post_command("Waiting","OFF")
    ###Arguments analysis
    if len(sys.argv) == 2 or len(sys.argv) == 4:
        if sys.argv[1] == "micro":
            procede = True
        elif sys.argv[1] == "arduino":
            microInput = False
            procede = True
        else:
            procede = False
        if len(sys.argv) == 4:
            if sys.argv[2] == "learn":
                procede = True
                learn = True
                result = sys.argv[3]
            else:
                procede = False
    if len(sys.argv) == 1:
        procede = True
    ###Parameters for analysis
    if microInput:
        HITLIMIT = 1000
        WAITLIMIT = 7
        BEGINCOUNT = 10
    else:
        HITLIMIT = 450
        WAITLIMIT = 7
        BEGINCOUNT = 5
        global xAr
        xAr = np.arange(0, 64)
    curWait = 0
    if procede:
        ml = MachineLearning(ls)
        app = QtGui.QApplication(sys.argv)
        win_plot = ui_plot.QtGui.QMainWindow()
        uiplot = ui_plot.Ui_win_plot()
        uiplot.setupUi(win_plot)
        uiplot.btnA.clicked.connect(plotSomething)
        uiplot.btnB.clicked.connect(lambda: uiplot.timer.setInterval(100.0))
        uiplot.btnC.clicked.connect(lambda: uiplot.timer.setInterval(10.0))
        uiplot.btnD.clicked.connect(lambda: uiplot.timer.setInterval(1.0))
        c = Qwt.QwtPlotCurve()
        c.attach(uiplot.qwtPlot)

        if microInput:
            ordo = 1000
        else:
            ordo = 1000
        uiplot.qwtPlot.setAxisScale(uiplot.qwtPlot.yLeft, 0, ordo)
        uiplot.timer = QtCore.QTimer()
        uiplot.timer.start(1.0)
        win_plot.connect(uiplot.timer, QtCore.SIGNAL('timeout()'), plotSomething)
        if microInput:
            SR = SwhRecorder()
            SR.setup()
            SR.continuousStart()
        else:
            AR = ArduinoReader()
            AR.continuousStart()
        ### DISPLAY WINDOWS
        win_plot.show()
        code = app.exec_()
        if microInput:
            SR.close()
        close_all()
    else:
        print(
        'Erreur dans les arguments: precisez l\'entree (\"micro\" ou \"arduino\") suivi de learn et de la valeur retour pour apprendre un echantillon.')
    close_all()