'''
 Copyright (c) 2016, Jack Miles Hunt
All rights reserved.
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
 * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
 * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
 * Neither the name of Jack Miles Hunt nor the
      names of contributors may be used to endorse or promote products
      derived from this software without specific prior written permission.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL Jack Miles Hunt BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''

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

if __name__ == "__main__":
    #Initialise matrices.
    transition = np.asarray([[1, 0], [0, 1]])
    control = np.identity(2)
    errorCov = np.identity(2)*0.2
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
