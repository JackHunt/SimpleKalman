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
