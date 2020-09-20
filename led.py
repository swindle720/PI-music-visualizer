#!/usr/bin/env python3
##########################
#       CONFIG
##########################
import pyaudio
import platform

NumLEDS = 600
StripLen = 8

if "Windows" in platform.platform():
    pi_mode = True
else:
    pi_mode = True

##########################

import time
from random import randrange
import numpy as np

if pi_mode is True:
    import board
    import neopixel
from threading import *


class color:
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)
    PINK = (153, 204, 255)
    ORANGE = (255, 165, 0)
    WHITE = (255, 255, 255)
    YELLOW = (255, 255, 0)
    NONE = (0, 0, 0)


class LED:
    LEDMemory = None
    last_LEDMemory = None

    StripLen = None
    NumLEDS = None
    PixelStream = None
    fftlen = 2 ** 11

    MIC_RATE = 44100
    FPS = 78

    LEDThread = None
    led_last_update = None

    def __init__(self, NUMLEDS, STRIPLEN):
        self.NumLEDS = NUMLEDS
        self.StripLen = STRIPLEN

        self.LEDMemory = [(0, 0, 0)] * NUMLEDS
        self.last_LEDMemory = [(0, 0, 0)] * NUMLEDS

        if pi_mode is True:
            self.PixelStream = neopixel.NeoPixel(board.D18, NUMLEDS, brightness=1.0, auto_write=False)
        self.led_last_update = time.time()

    def RandLED(self, array):
        return array[randrange(len(array))]

    def addLED(self, color):
        self.LEDMemory = np.insert(self.LEDMemory, 0, [color] * self.StripLen, axis=0)[:-self.StripLen, :]

    def updateLEDS(self):
        while True:
            if pi_mode is True:
                for i in range(self.NumLEDS):
                    self.PixelStream[i] = self.LEDMemory[i]
                self.PixelStream.show()
            else:
                print(self.last_LEDMemory[0])

    def BeatAlgorithm(self, beat, bass):
        Found_Beat = None

        if beat > 15:
            if  beat > 50:
                Found_Beat = True
                self.addLED(color.GREEN)
            elif Found_Beat is None and beat > 40:
                Found_Beat = True
                self.addLED(color.PINK)  # kore wa suki desu
            elif Found_Beat is None and beat > 20:
                Found_Beat = True
                self.addLED(color.NONE)
            elif Found_Beat is None and beat > 10:
                Found_Beat = True
                self.addLED(color.BLUE)
            elif Found_Beat is True and beat > 55:
                Found_Beat = False

        if Found_Beat is None and bass > 300 and bass < 700:
            Found_Beat = True
            self.addLED(color.RED)

        if Found_Beat is None:
            self.addLED(color.NONE)

    def microphone_update(self, audio_samples):
        fftvals = np.fft.rfft(audio_samples) * 2.0 / self.fftlen
        fftvals = np.abs(fftvals)

        levels = [np.sum(fftvals[0:100]) / 100,
                  np.sum(fftvals[100:1000]) / 900
                  ]

        bass = levels[0]
        beat = levels[1]

        self.BeatAlgorithm(beat, bass)

    def start_stream(self):
        self.LEDThread = Thread(target=self.updateLEDS).start()

        p = pyaudio.PyAudio()
        frames_per_buffer = int(self.MIC_RATE / self.FPS)
        stream = p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=self.MIC_RATE,
                        input=True,
                        frames_per_buffer=frames_per_buffer)
        while True:
            try:
                y = np.frombuffer(stream.read(frames_per_buffer, exception_on_overflow=False), dtype=np.int16)
                self.microphone_update(y)
            except IOError:
                pass

visualizer = LED(NumLEDS, StripLen)
visualizer.start_stream()