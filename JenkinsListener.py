#! /usr/bin/python
# coding=utf-8
import sys
import time
import RPi.GPIO as GPIO
try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen

cpt = 0 # Between 2 and 7 : simulation of commit in error
print("BOS project - get projectStatus on Jenkins")

# Init GPIO
# SET mode to use numerical position
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT, initial=GPIO.LOW)

try:
  while True:

    url = urlopen('https://fr.wikipedia.org/wiki/LoRaWAN')
    content = url.read()
    html_content = content.decode('utf8')

    # Commit in ERROR if "down" keyword is found (still found for the example)
    if html_content.find("down") != -1 and (cpt >= 2 and cpt <= 7):
      GPIO.output(4, GPIO.HIGH)
      print("### COMMIT in ERROR ###")
    elif cpt > 7:
      GPIO.output(4, GPIO.LOW)
      print("### NO ERROR ### Plus d'erreur à partir du 7ème appel")
    else:
      GPIO.output(4, GPIO.LOW)
      print("### NO ERROR ### Keep developping =)")

    cpt += 1
    # Wait 3 seconds
    time.sleep(3)

except KeyboardInterrupt:
  # Stop the light
  GPIO.output(4, GPIO.LOW)
  print(" => exit requested [CTRL + C]")
except:
  print("Detected exception : " + repr(sys.exc_info()))
