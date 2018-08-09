#!/usr/bin/env python2
import subprocess
import os
import signal
import RPi.GPIO as GPIO

from Reader import Reader

reader = Reader()
continue_reading = True

# get absolute path of this script
dir_path = os.path.dirname(os.path.realpath(__file__))


# Capture SIGINT for cleanup when the script is aborted
def end_read(signal, frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()


# Welcome message
print "Press Ctrl-C to stop."

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

playing = False
while continue_reading:
    # reading the card id
    cardid = reader.read_card()
    if cardid is None and playing:
        try:
            subprocess.call([dir_path + '/playout_controls.sh -c=playerstop'], shell=True)
            playing = False
        except OSError as e:
            print "Execution of stop failed:" + str(e)
    elif cardid is not None and not playing:
        try:
            # start the player script and pass on the card id
            subprocess.call([dir_path + '/rfid_trigger_play.sh --cardid=' + cardid], shell=True)
            playing = True
        except OSError as e:
            print "Execution of play failed:" + str(e)
#