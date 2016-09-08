#!/usr/bin/python3
from threading import Thread
import numpy as np
import UI as ui
import Kalman as kalman

class KalmanDemo(Thread):
    def __init__(self, ui, kf):
        Thread.__init__(self)
        self.__ui = ui
        self.__kf = kf

    def run(self):
        while self.__ui.shouldRun:#To-do add stopping condition.
            inputPoint = self.__ui.getDrawnPoint()
            if inputPoint not None:
                output = self.__kf.processPoint(inputPoint)
                self.__ui.pushKalmanPoint(output[0])

if __name__ == "__main__":
    #Initialise matrices.
#    transition = np.asarray()
#    control = np.asarray()
#    errorCov = np.asarray()
#    measureErrorCov = np.asarray()
#    initialMu = np.asarray()
#    initialSigma = np.asarray()

    #Initialise UI and kalman filter.
    ui = ui.UI(640, 480)
    kf = kalman.LinearKalmanFilter(transition, control, errorCov, measureErrorCov, initialMu, initialSigma)

    #Begin running the demo.
    demo = KalmanDemo(ui, kf)
    demo.start()
    demo.join()
