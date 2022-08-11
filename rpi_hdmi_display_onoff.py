#!python3
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time, sys, os, datetime, threading

## globals ###############

# Software debouncing
lastTime=datetime.datetime.now()
myBouncetime = 500.0 * 1000 #500ms

display_off_time = 10.0 * 60 # 10 minutes
init_time = 10.0 * 1000 * 1000 #10sec

# check if system is initalized (in this case wait some time)
start_time = datetime.datetime.now()

logfile = "/var/log/rpi_hdmi_display_onoff.log"

## functions #############

def log(string):
  now = datetime.datetime.now() # current date and time  
  timestamp = now.strftime("%b %d %H:%M:%S")
  with open(logfile, 'a') as file:
    file.write(timestamp + " " + string + "\n")
    file.close()

# Funktion definieren, um bei Tastendruck den
# LED-Zustand zu aendern
def switch_on(pin):
  #log("+switch_on() (bouncing button)")
  global lastTime
  now = datetime.datetime.now()
  # 500 ms Entprellzeit
  if now-lastTime > datetime.timedelta(microseconds=myBouncetime):
    log("detect debounced button")
    lastTime=datetime.datetime.now()
    power_state = get_hdmi_power_state()

    if power_state: power_state = 0
    else: power_state = 1

    log("get_hdmi_power_state() = " + str(get_hdmi_power_state()))
    log("set_hdmi_power_state() = " + str(power_state))
    set_hdmi_power_state(power_state)

    # after manual display on restart display off timer
    if power_state == 1:
        cancel_display_timer()
        start_display_timer()

  log("-switch_on()")

# set 0 for display off
# set 1 for display on
def set_hdmi_power_state(state):
  power = "vcgencmd display_power " + str(state)
  stream = os.popen(power)
  output = stream.read()

# return 0 or 1 as Integer parameter
def get_hdmi_power_state():
  stream = os.popen('vcgencmd display_power')
  output = stream.read()
  return int(output[14])

def display_timer():
  log("display timer")

  log("timer get_hdmi_power_state() = " + str(get_hdmi_power_state()))

  # only power off display with timer of init time is reached
  # it seems the hardware needs some seconds to report a correct status after system startup
#  now = datetime.datetime.now()
#  if now-start_time > datetime.timedelta(microseconds=init_time):   

  if get_hdmi_power_state() == 1:
    set_hdmi_power_state(0)
    log("set_hdmi_power_state(0)")

  start_display_timer()

def start_display_timer():
  global t
  t = threading.Timer(display_off_time , display_timer)
  t.start()

def cancel_display_timer():
  global t
  t.cancel()

## main ###############################

# use GPIO BCM  number!
GPIO.setmode(GPIO.BCM)

# BCM 27 = rpi_hdmi_display_onoff Button
GPIO.setup(27, GPIO.IN)

GPIO.setup(27, GPIO.IN, pull_up_down = GPIO.PUD_UP)

# switch_on-Funktion aufrufen, wenn Signal
# von HIGH auf LOW wechselt
GPIO.add_event_detect(27, GPIO.FALLING)
GPIO.add_event_callback(27, switch_on)

start_display_timer()

log("inital timer started")
log("initial get_hdmi_power_state() = " + str(get_hdmi_power_state()))

# mit minimaler CPU-Belastung auf das Programmende
# durch Strg+C warten
try:
  while True:
    time.sleep(5)
except KeyboardInterrupt:
  cancel_display_timer()
  GPIO.cleanup()
  sys.exit()


