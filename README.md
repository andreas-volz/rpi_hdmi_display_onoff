# Raspberry PI HDMI Display On/Off Button
Just a python script to control the HDMI display attached to a piCorePlayer

It might work with every Raspberry PI OS not only piCorePlayer.

Function is very easy. Attach a button to the configured PIN (BCM 27 by default) and when switching the display changes the on/off state.

At the same time there is a display sleep timer (default 10 minutes) to let the display go to sleep. This isn't perfect as it doesn't check for last touch input. Potential improvement. :-)
