# raspberry pi pwm fan control

* pwm control for orginal rapspberry pi fan
* support for fedora


## build container image

Build contaner image that includes:

* gpiod cli
* gpiod python module
* lgpio & rgpio python modules
* fan.py 

```
# podman build --tag gpio .
``` 

## run container

run container with fan.py 
```
# podman run -it --rm --name gpioexperiment --device=/dev/gpiochip0 localhost/gpio /usr/bin/python /src/fan.py --verbose
```

run container interactive
```
# podman run -it --rm --name gpioexperiment --device=/dev/gpiochip0 localhost/gpio /bin/bash

[root@074737ba6639 /]# /src/fan.py --help

fan.py [--min-temp=40] [--max-temp=70] [--fan-low=20] [--fan-high=100] [--wait-time=1] [--pwm-gpio=18] [--pwm-freq=10000] [--node-exporter] [-v|--verbose] [-h|--help]
```

run container with fan.py and node-exporter metrics (text file collector) for prometheus:
```
# podman run -d --rm --name raspberryfan -v /var/lib/node_exporter:/var/lib/node_exporter:z --device=/dev/gpiochip0 localhost/gpio /usr/bin/python /src/fan.py --node-exporter
```
note: be sure you have node exporter installed. Metrics will be written in /var/lib/node_exporter


start python fan.py script
```
# podman run -it --name gpioexperiment5 --rm -v /root/src:/src:z --device=/dev/gpiochip0 localhost/gpio python /src/fan.py
```

## gpiod

* https://fedoramagazine.org/turnon-led-fedora-iot/
* https://www.acmesystems.it/gpiod
* https://github.com/brgl/libgpiod/tree/master/bindings/python/examples

### gpiod cli
```
* gpiodetect - list all gpiochips present on the system, their names, labels
               and number of GPIO lines

* gpioinfo   - list all lines of specified gpiochips, their names, consumers,
               direction, active state and additional flags

* gpioget    - read values of specified GPIO lines

* gpioset    - set values of specified GPIO lines, potentially keep the lines
               exported and wait until timeout, user input or signal

* gpiofind   - find the gpiochip name and line offset given the line name

* gpiomon    - wait for events on GPIO lines, specify which events to watch,
               how many events to process before exiting or if the events
               should be reported to the console
```
### gpiod python

import gpiod



## lgpio

* https://github.com/joan2937/lg
* http://abyz.me.uk/lg/py_lgpio.html

### lgpio python

import lgpio

```
tx_pwm(handle, gpio, pwm_frequency, pwm_duty_cycle, pulse_offset=0, pulse_cycles=0)
This starts software timed PWM on an output GPIO.

Parameters

         handle:= >= 0 (as returned by gpiochip_open).
           gpio:= the GPIO to be pulsed.
  pwm_frequency:= PWM frequency in Hz (0=off, 0.1-10000).
 pwm_duty_cycle:= PWM duty cycle in % (0-100).
  pulse_offset:= offset from nominal pulse start position.
  pulse_cycles:= the number of cycles to be sent, 0 for infinite.


If OK returns the number of entries left in the PWM queue for the GPIO.

On failure returns a negative error code.

Each successful call to this function consumes one PWM queue entry.

pulse_cycles cycles are transmitted (0 means infinite).

PWM is characterised by two values, its frequency (number of cycles per second) and its dutycycle (percentage of high time per cycle).

pulse_offset is a microsecond offset from the natural start of the pulse cycle.

For instance if the PWM frequency is 10 Hz the natural start of each cycle is at seconds 0, then 0.1, 0.2, 0.3 etc. In this case if the offset is 20000 microseconds the cycle will start at seconds 0.02, 0.12, 0.22, 0.32 etc.

Another PWM command may be issued to the GPIO before the last has finished.

If the last pulse had infinite cycles then it will be replaced by the new settings at the end of the current cycle. Otherwise it will be replaced by the new settings when all its cycles are complete.

Multiple pulse settings may be queued in this way.
```
