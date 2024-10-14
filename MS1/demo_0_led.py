import sys
import time
from grove.grove_ryb_led_button import GroveLedButton

ledbtn = GroveLedButton(5)
nr_of_events = 4  # 0for infinite
flicks_per_event = 5
if len(sys.argv) == 1:
    print("Using default parameters")
elif len(sys.argv) == 3:
    nr_of_events = int(sys.argv[1])
    flicks_per_event = int(sys.argv[2])
else:
    info = """[ERROR] wrong number of argumentsYou need the pass 3 arguments:
    (arg 1 ) nrOfEvents (int)
    (arg 2) nrOfFlicksPerEvent (int)
    e.g.:
    $ python demo_0_led.py 4 5"""
    print(info)
    sys.exit()

print("Running demo ( {0} events,{1} flicks/event) ".format(nr_of_events, flicks_per_event))

for i in range(nr_of_events):
    print("firing event {0}".format(i + 1))
    for j in range(flicks_per_event):
        ledbtn.led.light(True)
        time.sleep(0.15)
        ledbtn.led.light(False)
        time.sleep(0.15)
    ledbtn.led.light(False)
    time.sleep(2)

print("Successfully finished led flicker program")