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
            if inputPoint != None:
                output = self.__kf.processPoint(np.asarray(inputPoint), np.asarray([0, 0]))
                point = output[0]
                self.__ui.pushKalmanPoint((int(point[0]), int(point[1])))
#                print(inputPoint)
                print(output[1])

if __name__ == "__main__":
    #Initialise matrices.
    transition = np.asarray([[1, 0], [0, 1]])
    control = np.identity(2)
    errorCov = np.identity(2)
    measureErrorCov = np.identity(2)*0.2
    initialMu = np.asarray([1, 1])
    initialSigma = np.identity(2)*0.2

    #Initialise UI and kalman filter.
    ui = ui.UI(640, 480)
    kf = kalman.LinearKalmanFilter(transition, control, errorCov, measureErrorCov, initialMu, initialSigma)

    #Begin running the demo.
    demo = KalmanDemo(ui, kf)
    demo.start()
    ui.start()
    demo.join()
