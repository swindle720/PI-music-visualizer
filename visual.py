import pygame
import random

import wave
import pyaudio
import numpy as np

from threading import *

pygame.init()
pygame.display.set_caption('LED Visualizer')

screen_W = 2000
screen_H = 500
screen_dot_size = 10
screen = pygame.display.set_mode([screen_W, screen_H])

def add_text(x,y, text):
    white = (255, 255, 255)
    green = (0, 255, 0)
    blue = (0, 0, 128)
    gray = (211, 211, 211)
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render(text, True, green, gray)
    textRect = text.get_rect()
    textRect.center = (x, y)

    return text, textRect

running = True

LEDS = 300

LEDMemory = [(0, 0, 0)] * LEDS
StripLen = 6

class color:
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)
    PINK = (255, 128, 255)
    ORANGE = (255, 165, 0)
    WHITE = (255, 255, 255)
    YELLOW = (255, 255, 0)
    NONE = (0, 0, 0)

def addLED(color):
    global LEDMemory
    global StripLen
    LEDMemory = np.insert(LEDMemory, 0, [color] * StripLen, axis=0)[:-StripLen, :]

bass = 0
beat = 0
unknown = 0

def music():
    global bass
    global beat
    global unknown

    CHUNK = 1024

    wf = wave.open("song.mp3", 'rb')

    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)


    data = wf.readframes(CHUNK)
    fftlen = 2**11

    while len(data) > 0:
        stream.write(data)
        data = wf.readframes(CHUNK)
        numpydata = np.frombuffer(data, dtype=np.int16)
        fftvals = np.fft.rfft(numpydata)*2.0/fftlen
        fftvals = np.abs(fftvals)

        levels = [np.sum(fftvals[0:80])/80/1000,
                  np.sum(fftvals[80:1000]) / 1000 / 10,
                  np.sum(fftvals[1000:2500]) / 1500
                  ]

        beat = levels[1]
        bass = levels[0]
        unknown = levels[2]

        Found_Beat = None

        if beat > 15:
            if beat > 140:
                Found_Beat = True
                addLED(color.NONE)
            elif Found_Beat is None and 50 > beat < 0:
                Found_Beat = True
                addLED(color.GREEN)
            elif Found_Beat is None and 80 > beat < 50:
                Found_Beat = True
                addLED(color.NONE) #kore wa suki desu
            elif Found_Beat is None and 110 > beat < 80:
                Found_Beat = True
                addLED(color.PINK)
            elif Found_Beat is None and 140 > beat < 110:
                Found_Beat = True
                addLED(color.PINK)

        if Found_Beat is None and bass > 0.30:
            Found_Beat = True
            addLED(color.RED)

        if Found_Beat is None:
            addLED(color.NONE)

    stream.stop_stream()
    stream.close()
    p.terminate()

LEDThread = Thread(target=music).start()

game_LED_location = []

def setuplocations():
    h = 100
    w = 0

    rows = 35

    W_fit = int(screen_W / ((LEDS * screen_dot_size * 2) / rows)) * 2

    print(W_fit)

    flip_state = False

    for i in range(LEDS):

        if flip_state is False:
            w = w + W_fit

        if flip_state is True:
            w = w - W_fit

        if w <= 0:
            flip_state = False
            h = h + screen_dot_size * 10
        elif w >= screen_W:
            flip_state = True
            h = h + screen_dot_size * 10

        game_LED_location.append((int(w), int(h)))

setuplocations()

while running:

    led_list = []

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False

    screen.fill((211, 211, 211))

    text, textRect = add_text(150, 480, "Bass: {:0.2f}".format(bass))
    screen.blit(text, textRect)

    text, textRect = add_text(350, 480, "Beat: {:0.2f}".format(beat))
    screen.blit(text, textRect)

    text, textRect = add_text(600, 480, "Beat: {:0.2f}".format(unknown))
    screen.blit(text, textRect)

    screen.blit(text, textRect)

    for i in range(len(game_LED_location)):
        pygame.draw.circle(screen, LEDMemory[i], game_LED_location[i], screen_dot_size)

    pygame.display.flip()


# Done! Time to quit.

pygame.quit()
