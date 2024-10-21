import time
from grove.grove_ryb_led_button import GroveLedButton
 
def main():
    ledbtn = GroveLedButton(18)
    n = 0
    while True:
        ledbtn.led.light(True)
        time.sleep(1)
 
        ledbtn.led.light(False)
        time.sleep(1)
        n += 1
        if n == 3:
            break
        
 
if __name__ == '__main__':
    main()
