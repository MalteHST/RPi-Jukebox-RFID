#!/usr/bin/env python
#coding: utf8

import subprocess
import os
import lirc
import time

sockid = lirc.init('remote', blocking=False)

# get absolute path of this script
dir_path = os.path.dirname(os.path.realpath(__file__))

while True:
    codeIR = lirc.nextcode()
    if codeIR != []:
        try:
            subprocess.call([dir_path + '/rfid_trigger_play.sh --cardid=' + codeIR[0]], shell=True)
        except OSError as e:
            print "Execution failed:" + str(e)
    time.sleep(0.05)

