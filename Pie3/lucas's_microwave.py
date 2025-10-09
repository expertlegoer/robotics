import RPi.GPIO as gpio
import keypad
import LCD
import time

kp = keypad.keypad(4)
lcd = LCD.LCD()
delay = 0.2
delay2 = 0.252
delay3 = 1


gpio.setmode(gpio.BOARD)
motorPin = 18
soundThingy = 40
gpio.setup(soundThingy, gpio.OUT)

gpio.setup(motorPin,gpio.OUT)
motor = gpio.PWM(motorPin, 100)
motor.start(0)

lcd.message("Please enter", 1)
lcd.message("cooking time!", 2)

raw = ""
motor.start(0)

while(True):
    digit = kp.getKey()
    if(digit!= None):
        
        if(str(digit) == "*"):
            break
        raw += str(digit)
        if(len(raw)==1):
            formatted="00:0" + str(raw)
            lcd.clear()
            lcd.message(formatted)
        if(len(raw)==2):
            formatted="00:" + str(raw)
            lcd.clear()
            lcd.message(formatted)
        if(len(raw)==3):
            formatted="0" + str(raw)[0]+":"+str(raw)[1:]
            lcd.clear()
            lcd.message(formatted)
        if(len(raw)==4):
            formatted=str(raw)[0:2]+":"+str(raw)[2:]
            lcd.clear()
            lcd.message(formatted)
            break
        time.sleep(delay)

if(len(str(raw)) == 4):
    minutes = int(str(raw)[0:2]) * 60
    seconds = int(str(raw)[2:])
if(len(str(raw)) == 3):
    minutes = int(str(raw)[0:1]) * 60
    seconds = int(str(raw)[1:])
if(len(str(raw)) == 2):
    minutes = 0
    seconds = int(str(raw))
if(len(str(raw)) == 1):
    minutes = 0
    seconds = int(str(raw))
if(len(str(raw)) == 0):
    minutes = 0
    seconds = 0
total = int(minutes) + int(seconds)
start = time.time()
motor.ChangeDutyCycle(12.5)
while(True):
    end = time.time()
    elapsed = end - start
    remaining = int(total-elapsed)

    minutes = remaining // 60
    seconds = remaining % 60

    if(len(str(minutes)) ==1):
        minutes = "0"+str(minutes)
    if(len(str(seconds)) ==1):
        seconds = "0"+str(seconds)

    formatted = str(minutes) + ":" + str(seconds)
    lcd.message(formatted)

    if(remaining <=0):
        motor.ChangeDutyCycle(0)
        gpio.output(soundThingy,True)
        print("beep")
        time.sleep(delay2)
        gpio.output(soundThingy,False)
        print("no beep ur trash")
        time.sleep(delay2)
        gpio.output(soundThingy,True)
        print("beep")
        time.sleep(delay2)
        gpio.output(soundThingy,False)
        print("no beep ur trash")
        time.sleep(delay2)
        gpio.output(soundThingy,True)
        print("beep")
        time.sleep(delay3)
        gpio.output(soundThingy,False)
        print("no beep ur trash")
        time.sleep(delay2)
        break
