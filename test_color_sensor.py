#! /usr/bin/python

import smbus
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

#LED is connected to GPIO 23
led_pin = 23
GPIO.setup(led_pin, GPIO.OUT)
GPIO.output(led_pin, True)
bus = smbus.SMBus(1)

bus.write_byte(0x29,0x80|0x12)
ver = bus.read_byte(0x29)

if ver != 0x44:
   print "No device detected"

bus.write_byte(0x29, 0x80|0x00)  # ENABLE register
bus.write_byte(0x29, 0x01|0x02)  # 
bus.write_byte(0x29, 0x80|0x14)

print "Intensity\tRed\tGreen\tBlue"
count = 0
while count < 10:
   #GPIO.output(led_pin, True)
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
   count += 1
GPIO.output(led_pin, False)  

