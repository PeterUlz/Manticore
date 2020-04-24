#! /usr/bin/python

# Test step motor
import smbus
import sys
import time
import RPi.GPIO as GPIO
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

GPIO.setmode(GPIO.BCM)

led_pin = 23
GPIO.setup(led_pin, GPIO.OUT)
GPIO.output(led_pin, True)
bus = smbus.SMBus(1)

bus.write_byte(0x29,0x80|0x12)
ver = bus.read_byte(0x29)

StepPins =[17,18,27,22]

for pin in StepPins:
   print "Setup pins"
   GPIO.setup(pin, GPIO.OUT)
   GPIO.output(pin, False)

#Define advanced sequence as shown in
#  manufucaturers datasheet

Seq = [[1,0,0,1],
       [1,0,0,0],
       [1,1,0,0],
       [0,1,0,0],
       [0,1,1,0],
       [0,0,1,0],
       [0,0,1,1],
       [0,0,0,1]]



def get_color():
   time.sleep(0.2)
   data = bus.read_i2c_block_data(0x29,0)
   clear = clear = data[1] << 8 | data[0]
   red = data[3] << 8 | data[2]
   green = data[5] << 8 | data[4]
   blue = data[7] << 8 | data[6]
   crgb = str(clear)+"\t"+str(red)+"\t"+str(green)+"\t"+str(blue)
   #rgb = str(100.*float(red)/float(clear))+"\t"+str(100.*float(green)/float(clear))+"\t"+str(100.*float(blue)/float(clear))
   print crgb
   #GPIO.output(led_pin, False)   
   time.sleep(1)
   return clear, red, green, blue

colors = []
values = []
index  = []

def plot_seq(colors, index, values):
    data = pd.DataFrame({"Color": colors,
                         "Values": values,
                         "Index": index})
    sns.barplot(x="Index", y="Values", hue="Color", data=data)
    plt.savefig("Run.jpeg")

StepCount = len(Seq)
StepDir = 1

StepCounter = 0
total_steps = 0
color_count = 0

while True:
   # print StepCounter
   # print Seq[StepCounter]
   for pin in range(0,4):
      xpin = StepPins[pin]
      if Seq[StepCounter][pin] != 0:
         # print "Enable GPIO %i" %(xpin)
         GPIO.output(xpin, True)
      else:
         # print "Disable GPIO %i" %(xpin)
         GPIO.output(xpin, False)

   StepCounter += StepDir
   total_steps += StepDir
   if (StepCounter >= StepCount):
      StepCounter = 0
   if StepCounter < 0:
      StepCounter = StepCount+StepDir

   time.sleep(0.004)
   if total_steps % 300 == 0:
        clear, red, green, blue = get_color()
        color_count += 1
        colors.extend(["clear","red","green","blue"])
        values.extend([clear, red, green, blue])
        index.extend([color_count]*4)

   if color_count == 30:
       break

plot_seq(colors, index, values)
GPIO.output(led_pin, False)  
for pin in StepPins:
   print "Setup pins"
   GPIO.setup(pin, GPIO.OUT)
   GPIO.output(pin, False)  