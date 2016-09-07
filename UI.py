#!/usr/bin/python3
import tkinter as tk

class UI:
    __drawnPoints = []
    
    def __init__(self, width, height):
        self.__window = tk.Tk()
        self.__canvas = tk.Canvas(self.__window, width=width, height=height, bg="black")
        self.__canvas.pack()
        self.__window.title("Kalman Filter Demo")
        self.__window.geometry(str(width)+"x"+str(height))
        self.__window.bind("<B1-Motion>", self.__mouseMoveCallback)
        self.__draw()
        self.__window.mainloop()

    def __mouseMoveCallback(self, event):
        self.__drawnPoints.append(event.x)
        self.__drawnPoints.append(event.y)
        
    def __draw(self):
        if len(self.__drawnPoints) > 1 and len(self.__drawnPoints) % 2 == 0:
            self.__canvas.delete("all")
            self.__canvas.create_line(self.__drawnPoints, fill="green")
        self.__window.after(32, self.__draw)
        
if __name__ == "__main__":
    ui = UI(640, 480)
