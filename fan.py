#!/usr/bin/python

# python modules
import lgpio as sbc
import time
import signal
import sys
import os
import sys, getopt

# Configuration
PWM_GPIO_NR = 18        # PWM gpio number used to drive PWM fan (gpio18 = pin 12)
WAIT_TIME = 1           # [s] Time to wait between each refresh
PWM_FREQ = 10000        # [Hz] 10kHz for Noctua PWM control

# Configurable temperature and fan speed
MIN_TEMP = 40
MAX_TEMP = 60
FAN_LOW = 20
FAN_HIGH = 100
FAN_OFF = 0
FAN_MAX = 100

# logging and metrics (enable = 1)
VERBOSE = 0
NODE_EXPORTER = 0

# parse input arguments
try:
   opts, args = getopt.getopt(sys.argv[1:],"hv",["min-temp=","max-temp=","fan-low=","fan-high=","wait-time=","help","pwm-gpio=","pwm-freq=","verbose","node-exporter"])
except getopt.GetoptError:
   print('fan.py [--min-temp=40] [--max-temp=70] [--fan-low=20] [--fan-high=100] [--wait-time=1] [--pwm-gpio=18] [--pwm-freq=10000] [--node-exporter] [-v|--verbose] [-h|--help]')
   sys.exit(2)
for opt, arg in opts:
   if opt in ("-h", "--help"):
      print('fan.py [--min-temp=40] [--max-temp=70] [--fan-low=20] [--fan-high=100] [--wait-time=1] [--pwm-gpio=18] [--pwm-freq=10000] [--node-exporter] [-v|--verbose] [-h|--help]')
      sys.exit()
   elif opt in ("-v", "--verbose"):
      VERBOSE = 1
   elif opt in ("--min-temp"):
      MIN_TEMP = int(arg)
   elif opt in ("--max-temp"):
      MAX_TEMP = int(arg)
   elif opt in ("--fan-low"):
      FAN_LOW = int(arg)
   elif opt in ("--fan-high"):
      FAN_HIGH = int(arg)
   elif opt in ("--wait-time"):
      WAIT_TIME = int(arg)
   elif opt in ("--pwm-gpio"):
      PWM_GPIO_NR = int(arg)
   elif opt in ("--pwm-freq"):
      PWM_FREQ = int(arg)
   elif opt in ("--node-exporter"):
      NODE_EXPORTER = 1
print("")
print("MIN_TEMP:",MIN_TEMP)
print("MAX_TEMP:",MAX_TEMP)
print("FAN_LOW:",FAN_LOW)
print("FAN_HIGH:",FAN_HIGH)
print("WAIT_TIME:",WAIT_TIME)
print("PWM_GPIO_NR:",PWM_GPIO_NR)
print("PWM_FREQ:",PWM_FREQ)
print("VERBOSE:",VERBOSE)
print("NODE_EXPORTER:",NODE_EXPORTER)
print("")

# Get CPU's temperature
def getCpuTemperature():
    res = os.popen('cat /sys/devices/virtual/thermal/thermal_zone0/temp').readline()
    temp = (float(res)/1000)
    return temp

# Set fan speed
def setFanSpeed(speed,temp):
    sbc.tx_pwm(fan , PWM_GPIO_NR, PWM_FREQ, speed, pulse_offset=0, pulse_cycles=0)

    # print fan speed and temperature
    if VERBOSE == 1:
        print("fan speed: ",int(speed),"    temp: ",temp)

    # write fan metrics to file for node-exporter/prometheus
    if NODE_EXPORTER == 1:
        # Save a reference to the original standard output
        original_stdout = sys.stdout 
        with open('/var/lib/node_exporter/fan-metrics.prom', 'w') as f:
            # Change the standard output to the file we created.
            sys.stdout = f 
            print('raspberry_fan_speed ',speed)
            print('raspberry_fan_temp ',temp)
            print('raspberry_fan_min_temp ',MIN_TEMP)
            print('raspberry_fan_max_temp ',MAX_TEMP)
            print('raspberry_fan_fan_low ',FAN_LOW)
            print('raspberry_fan_fan_high ',FAN_HIGH)
            print('raspberry_fan_wait_time ',WAIT_TIME)
            print('raspberry_fan_pwm_gpio ',PWM_GPIO_NR)
            print('raspberry_fan_freq ',PWM_FREQ)
            # Reset the standard output to its original value
            sys.stdout = original_stdout
            f.close()

    return()

# Handle fan speed
def handleFanSpeed():
    temp = getCpuTemperature()

    # Turn off the fan if temperature is below MIN_TEMP
    if temp < MIN_TEMP:
        setFanSpeed(FAN_OFF,temp)

    # Set fan speed to MAXIMUM if the temperature is above MAX_TEMP
    elif temp > MAX_TEMP:
        setFanSpeed(FAN_MAX,temp)

    # Caculate dynamic fan speed
    else:
        step = (FAN_HIGH - FAN_LOW)/(MAX_TEMP - MIN_TEMP)   
        delta = temp - MIN_TEMP
        speed = FAN_LOW + ( round(delta) * step )
        setFanSpeed(speed,temp)

    return ()

try:
    # Setup GPIO pin
    fan = sbc.gpiochip_open(0)
    sbc.gpio_claim_output(fan, PWM_GPIO_NR)
    setFanSpeed(FAN_LOW,MIN_TEMP)

    # Handle fan speed every WAIT_TIME sec
    while True:
        handleFanSpeed()
        time.sleep(WAIT_TIME)

except KeyboardInterrupt: # trap a CTRL+C keyboard interrupt
    setFanSpeed(FAN_LOW,MIN_TEMP)
