#! /usr/bin/python

# Test step motor
import sys
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

StepPins =[17,18,27,22]

for pin in StepPins:
   print "Setup pins"
   GPIO.setup(pin, GPIO.OUT)
   GPIO.output(pin, False)
