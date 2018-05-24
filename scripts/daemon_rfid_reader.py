import subprocess
import os 
from Reader import Reader

reader = Reader()

# get absolute path of this script
dir_path = os.path.dirname(os.path.realpath(__file__))

print dir_path

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

while continue_reading:
    # reading the card id
    cardid = reader.read_card()
    if cardid is not None:
        subprocess.call(['aplay ' + dir_path + '/../misc/robot_blip.wav'], shell=True)
        try:
            # start the player script and pass on the card id
            subprocess.call([dir_path + '/rfid_trigger_play.sh --cardid=' + cardid], shell=True)
        except OSError as e:
            print "Execution failed:" + str(e)
