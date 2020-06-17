# Raspberry Pi 3+ LED(WS2812B) Realtime Music Visualizer

This is a simple LED Visualizer using raspberry PI. I recommend to install just the ubuntu server on your PI as this script uses about 80% of your CPU. These scripts allow your raspberry PI to control LEDs(WS2812B) over wifi. The client (Your computer) connects using sockets and sends the frequency levels to your server (raspberry PI). The server then outputs to the LEDS giving you a Realtime Music Visualizer. There is currently no limit to how many LEDS you can control but you will need a good power supply.

1 LED can use up to 60milamp

In my case I needed 5V 40amp (200w) power supply for 1200 LED'S

## Enable GPIO pins

```bash
sudo raspi-config
```
Advanced options

I2c

Enable I2c

## Installations
You will need to install Python 3.5+ There are plenty of guides on how to do this online, I may add a detailed guide at some point.

## Install missing Packages
```python
pip install adafruit-circuitpython-neopixel
pip install numpy
```

## Server Configuration

Edit your to suit your needs on both server.py and client.py

Address_Server, Address_Port must be the same on both files.

```python

DebugMode = False #Keep this false
NumLEDS = 120 #
StripLen = 6

Address_Server = "192.168.1.9" #local network address
Address_Port = 1226
```
Upload server.py to your raspberry pi

Run with this command below

```bash
sudo python3 server.py
```

Plug your LED dataline to GPIO 18 (pin 6) on your raspberry pi See images online.


## Client Configuration


Run the client with python3 using idle or some other IDE. 

```bash
sudo python3 client.py
```


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

This project is being worked on and getting improved when I get free time.

## License
[MIT](https://choosealicense.com/licenses/mit/)
