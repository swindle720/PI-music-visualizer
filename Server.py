##########################
#       CONFIG
##########################
DebugMode = False
NumLEDS = 120
StripLen = 6
##########################
import time
from _thread import *
from threading import *
import socket
from random import randrange
import numpy as np
import pickle

if DebugMode is False:
    import board
    import neopixel

if DebugMode:
    Address_Server = "127.0.0.1"
    Address_Port = 12345
else:
    Address_Server = "192.168.1.9"
    Address_Port = 1226


class color:
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)
    PINK = (255, 128, 255)
    ORANGE = (255, 165, 0)
    WHITE = (255, 255, 255)
    YELLOW = (255, 255, 0)
    NONE = (0, 0, 0)


class Server:
    LEDMemory = [(0, 0, 0)] * NumLEDS
    HasConnection = False #Client Connection
    StripLen = None
    NumLEDS = None
    PixelStream = None
    DebugMode = None
    LEDThread = None #Thread Var

    def __init__(self, NUMLEDS, STRIPLEN, Debug_mode=False):
        self.NumLEDS = NUMLEDS
        self.StripLen = STRIPLEN
        self.Debug_mode = Debug_mode

        if Debug_mode == False:
            self.PixelStream = neopixel.NeoPixel(board.D18, NUMLEDS, auto_write=False)

    def RandLED(self, array):
        return array[randrange(len(array))]

    def addLED(self, color):
        self.LEDMemory = np.insert(self.LEDMemory, 0, [color] * self.StripLen, axis=0)[:-self.StripLen, :]

    def updateLEDS(self):
        while True:
            if self.HasConnection is False:
                if self.Debug_mode is False: #Set all LEDS back to None
                    for i in range(self.NumLEDS):
                        self.PixelStream[i] = color.NONE
                    self.PixelStream.show()
                break

            if self.Debug_mode is False:
                for i in range(self.NumLEDS):
                    self.PixelStream[i] = self.LEDMemory[i]
                self.PixelStream.show()

    def clienthandler(self, c):
        while True:
            try:
                data = pickle.loads(c.recv(1024))
                if not data:
                    print('Bye')
                    break

                bass, beat, unknown = data

                Found_Beat = None

                if beat > 15:
                    if beat > 60:
                        Found_Beat = True
                        self.addLED(color.NONE)
                    elif beat > 50:
                        Found_Beat = True
                        self.addLED(color.PINK)
                    elif beat > 40:
                        Found_Beat = True
                        self.addLED(color.WHITE)
                    elif Found_Beat is None and beat > 30:
                        Found_Beat = True
                        self.addLED(color.BLUE)
                    elif Found_Beat is None and beat > 20:
                        Found_Beat = True
                        self.addLED(color.GREEN)
                    elif Found_Beat is None:
                        Found_Beat = True
                        self.addLED(color.ORANGE)

                if bass > 240 and bass < 320:
                    Found_Beat = True
                    self.addLED(color.RED)

                if Found_Beat is None:
                    self.addLED(color.NONE)
            except:  # not the best idea but w/e
                print("Connection Dropped")
                self.HasConnection = False
                break

        c.close()

    def Start(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((Address_Server, Address_Port))
        s.listen()

        while True:
            # establish connection with client
            conn, addr = s.accept()
            if conn and self.HasConnection is False: #Lets accept one connection only
                self.HasConnection = True
                self.LEDThread = Thread(target=self.updateLEDS).start()
                print('Connected to :', addr[0], ':', addr[1])
                Thread(target=self.clienthandler, args=(conn,)).start()

srv = Server(NumLEDS, StripLen, DebugMode)
srv.Start()