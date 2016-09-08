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

import tkinter as tk
from queue import Queue

class UI:
    def __init__(self, width, height):
        self.shouldRun = True
        self.__drawnPoints = []
        self.__kalmanPoints = []
        self.__inputQueue = Queue()
        self.__kalmanQueue = Queue()
        self.__window = tk.Tk()
        self.__canvas = tk.Canvas(self.__window, width=width, height=height, bg="black")
        self.__canvas.pack()
        self.__window.title("Kalman Filter Demo")
        self.__window.geometry(str(width)+"x"+str(height))
        self.__window.bind("<B1-Motion>", self.__mouseMoveCallback)
        self.__window.protocol("WM_DELETE_WINDOW", self.__exitCallback)
        self.__updateKalmanPoints()
        self.__draw()

    def __mouseMoveCallback(self, event):
        self.__drawnPoints.append(event.x)
        self.__drawnPoints.append(event.y)
        self.__inputQueue.put((event.x, event.y))

    def __updateKalmanPoints(self):
        while not self.__kalmanQueue.empty():
            self.__kalmanPoints.append(self.__kalmanQueue.get())
        self.__window.after(16, self.__updateKalmanPoints)
        
    def __draw(self):
        if len(self.__drawnPoints) > 3:
            self.__canvas.delete("all")
            self.__canvas.create_line(self.__drawnPoints, fill="green")

        if len(self.__kalmanPoints) > 3:
            self.__canvas.create_line(self.__kalmanPoints, fill="red")
            
        self.__window.after(32, self.__draw)

    def __exitCallback(self):
        self.shouldRun = False

    def getDrawnPoint(self):
        if not self.__inputQueue.empty():
            return self.__inputQueue.get()
        return None

    def pushKalmanPoint(self, point):
        self.__kalmanQueue.put(point)

    def start(self):
        self.__window.mainloop()
