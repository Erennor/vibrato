import ui_plot
import sys
import numpy
from scipy import stats
from PyQt4 import QtCore, QtGui
import PyQt4.Qwt5 as Qwt
from recorder import *
import peak_detect as peak
import os
from math import *


def plotSomething():
    if SR.newAudio==False: 
        return
    xs,ys=SR.fft()
    c.setData(xs,ys)
    uiplot.qwtPlot.replot()
    ### START peak detection ###
    _max, _min = peak.peakdetect(ys, xs, 30, 0.30)
    slope, intercept, r_value, p_value, std_err = stats.linregress(xs,ys)
    THRESHOLD = 10000
    thresholdIsReached = ys > THRESHOLD
    thresholdIsReached[1:][thresholdIsReached[:-1] & thresholdIsReached[1:]] = False
    iterateur = 1
    if thresholdIsReached.any():
		print "Lin Reg: ", slope, "Peaks detected: ",_max
		print "iterateur: ", iterateur
		if iterateur%2==0:
		    os.system('curl --header "Content-Type: text/plain" --request PUT --data "ON" http://localhost:8080/rest/items/Light_Gest/state')
		else:
		    print "off"
		    os.system('curl --header "Content-Type: text/plain" --request PUT --data "OFF" http://localhost:8080/rest/items/Light_Gest/state') 
    ### END peak detection ###
    SR.newAudio=False

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    win_plot = ui_plot.QtGui.QMainWindow()
    uiplot = ui_plot.Ui_win_plot()
    uiplot.setupUi(win_plot)
    uiplot.btnA.clicked.connect(plotSomething)
    uiplot.btnB.clicked.connect(lambda: uiplot.timer.setInterval(100.0))
    uiplot.btnC.clicked.connect(lambda: uiplot.timer.setInterval(10.0))
    uiplot.btnD.clicked.connect(lambda: uiplot.timer.setInterval(1.0))
    c=Qwt.QwtPlotCurve()
    c.attach(uiplot.qwtPlot)
    
    uiplot.qwtPlot.setAxisScale(uiplot.qwtPlot.yLeft, 0, 1000)
    
    uiplot.timer = QtCore.QTimer()
    uiplot.timer.start(1.0)
    
    win_plot.connect(uiplot.timer, QtCore.SIGNAL('timeout()'), plotSomething) 
    
    SR=SwhRecorder()
    SR.setup()
    SR.continuousStart()

    ### DISPLAY WINDOWS
    win_plot.show()
    code=app.exec_()
    SR.close()
    sys.exit(code)
