import wave
import pyaudio
import socket
import numpy as np
import pickle
import atexit

Debug_mode = False

if Debug_mode:
    Address_Server = "127.0.0.1"
    Address_Port = 12345
else:
    Address_Server = "192.168.1.9"
    Address_Port = 1226

class bcolors: #not in use anymore
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def Client():
    CHUNK = 1024

    udp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    udp.connect((Address_Server, Address_Port))

    def exit_handler():
        udp.close()
        print('My application is ending!')

    atexit.register(exit_handler)

    wf = wave.open("heartbroken.wav", 'rb')

    # instantiate PyAudio (1)
    p = pyaudio.PyAudio()

    # open stream (2)
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    # read data
    data = wf.readframes(CHUNK)
    fftlen = 2**11
    # play stream (3)
    while len(data) > 0:
        stream.write(data)
        data = wf.readframes(CHUNK)
        numpydata = np.frombuffer(data, dtype=np.int16)
        fftvals = np.fft.rfft(numpydata)*2.0/fftlen
        fftvals = np.abs(fftvals)

        levels = [np.sum(fftvals[0:100])/100,
                  np.sum(fftvals[100:1000]) / 400,
                  np.sum(fftvals[1000:2500]) / 1500
                  ]

        bass = levels[0]
        beat = levels[1]
        unknown = levels[2]

        SendData = [0, 0, 0]

        SendData[0] = bass
        SendData[1] = beat
        SendData[2] = unknown

        udp.sendall(pickle.dumps(SendData))

    # stop stream (4)
    stream.stop_stream()
    stream.close()
    # close PyAudio (5)
    p.terminate()

Client()