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

#Define advanced sequence as shown in
#  manfucaturers datasheet

Seq = [[1,0,0,1],
       [1,0,0,0],
       [1,1,0,0],
       [0,1,0,0],
       [0,1,1,0],
       [0,0,1,0],
       [0,0,1,1],
       [0,0,0,1]]

StepCount = len(Seq)
StepDir = 1

StepCounter = 0

while True:
   print StepCounter
   print Seq[StepCounter]
   for pin in range(0,4):
      xpin = StepPins[pin]
      if Seq[StepCounter][pin] != 0:
         print "Enable GPIO %i" %(xpin)
         GPIO.output(xpin, True)
      else:
         print "Disable GPIO %i" %(xpin)
         GPIO.output(xpin, False)

   StepCounter += StepDir

   if (StepCounter >= StepCount):
      StepCounter = 0
   if StepCounter < 0:
      StepCounter = StepCount+StepDir

   time.sleep(0.004)


   