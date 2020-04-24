#! python3

# Start Sequencing run on LEGO sequencer 

import smbus
import sys
import time
import RPi.GPIO as GPIO
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import argparse


def get_color():
   time.sleep(0.2)
   data = bus.read_i2c_block_data(0x29,0)
   clear = data[1] << 8 | data[0]
   red = data[3] << 8 | data[2]
   green = data[5] << 8 | data[4]
   blue = data[7] << 8 | data[6]
   crgb = str(clear)+"\t"+str(red)+"\t"+str(green)+"\t"+str(blue)
   #rgb = str(100.*float(red)/float(clear))+"\t"+str(100.*float(green)/float(clear))+"\t"+str(100.*float(blue)/float(clear))
   print(crgb)
   #GPIO.output(led_pin, False)   
   time.sleep(1)
   return clear, red, green, blue

def save_data(colors, index, values, prefix):
    data = pd.DataFrame({"Color": colors,
                         "Values": values,
                         "Index": index})
    data.to_csv(prefix+".csv")

def plot_seq_sns(colors, index, values, prefix):
    data = pd.DataFrame({"Color": colors,
                         "Values": values,
                         "Index": index})
    sns.barplot(x="Index", y="Values", hue="Color", data=data)
    plt.savefig(prefix+"_sns.png")
    plt.clf()


def plot_seq(colors, index, values, prefix):
    data = pd.DataFrame({"Color": colors,
                         "Values": values,
                         "Index": index})
    #sns.barplot(x="Index", y="Values", hue="Color", data=data)
    #plt.savefig("Run.jpeg")
    index = list(set(data["Index"]))
    red = data["Color"] == "red"
    plt.bar(index, data["Values"][red], fill="red")
    green = data["Color"] == "green"
    plt.bar(index, data["Values"][green], fill="green")
    blue = data["Color"] == "blue"
    plt.bar(index, data["Values"][blue], fill="blue")
    plt.savefig(prefix+".png")
    plt.clf()



def plot_seq_norm(colors, index, values, prefix):
    data = pd.DataFrame({"Color": colors,
                         "Values": values,
                         "Index": index})
    index = list(set(data["Index"]))
    index_sum = [np.sum(data["Values"][data["Index"] == i]) for i in index]
    red = data["Color"] == "red"
    plt.bar(index, data["Values"][red]/index_sum, fill="red")
    green = data["Color"] == "green"
    plt.bar(index, data["Values"][green]/index_sum, fill="green")
    blue = data["Color"] == "blue"
    plt.bar(index, data["Values"][blue]/index_sum, fill="blue")
    plt.savefig(prefix+"_norm.png")
    plt.clf()

def run(max_color_counts):
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
            #   print "Enable GPIO %i" %(xpin)
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

        if color_count > max_color_counts:
            return colors, index, values


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--out_dir', type=str, required=True,
                    help='Output directory')
    parser.add_argument('--prefix', type=str, required=True,
                    help='Prefix for plots')
    parser.add_argument('--max_reads', dest='max_reads',
                    type=int, default=100,
                    help='max color readings')

    args = parser.parse_args()


    GPIO.setmode(GPIO.BCM)
    led_pin = 23
    GPIO.setup(led_pin, GPIO.OUT)
    GPIO.output(led_pin, True)
    bus = smbus.SMBus(1)

    bus.write_byte(0x29,0x80|0x12)
    ver = bus.read_byte(0x29)

    StepPins =[17,18,27,22]

    for pin in StepPins:
        print("Setup pins")
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


    
    colors = []
    values = []
    index  = []

    colors, index, values = run(args.max_reads)
    plot_seq(colors, index, values, args.prefix)
    plot_seq_norm(colors, index, values, args.prefix)
    plot_seq_sns(colors, index, values, args.prefix)
    GPIO.output(led_pin, False)
    save_data(colors, index, values, args.prefix) 
    for pin in StepPins:
        print("Setup pins")
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, False)  
