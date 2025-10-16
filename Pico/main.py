import utime
from machine import I2C, Pin, PWM
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd

motor_pin = PWM(Pin(0))
motor = PWM(Pin(0))
buzzer = Pin(15, Pin.OUT)
motor.freq(1000)

i2c = I2C(0, sda=Pin(4), scl=Pin(5)) # Use GP4 for SDA, GP5 for SCL
I2C_ADDR = 0X27
NUM_ROWS = 2
NUM_COLS = 16
lcd = I2cLcd(i2c,I2C_ADDR, NUM_ROWS, NUM_COLS)
delay = 0.2
#i2c
#lcd.putstr("I got it to work !")

matrix_keys = [['1', '2', '3', 'A'],
               ['4', '5', '6', 'B'],
               ['7', '8', '9', 'C'],
               ['*', '0', '#', 'D']]

# PINs according to schematic - Change the pins to match with your connections
keypad_rows = [6,7,8,9]
keypad_columns = [10,11,12,13]

# Create two empty lists to set up pins ( Rows output and columns input )
col_pins = []
row_pins = []

# Loop to assign GPIO pins and setup input and outputs
for x in range(0,4):
    row_pins.append(Pin(keypad_rows[x], Pin.OUT))
    row_pins[x].value(1)
    col_pins.append(Pin(keypad_columns[x], Pin.IN, Pin.PULL_DOWN))
    col_pins[x].value(0)
    
##############################Scan keys ####################
    
print("Please enter a key from the keypad")
    
def scankeys():  
    for row in range(4):
        for col in range(4):
            row_pins[row].high()
            key = None
            
            if col_pins[col].value() == 1:
                print("You have pressed:", matrix_keys[row][col])
                key_press = matrix_keys[row][col]
                return key_press
                
                    
        row_pins[row].low()
lcd.clear()
lcd.putstr("Enter Time")
raw = ""
#motor.start(0)
while True:
   digit = scankeys()
   
   if digit != None:
       #nothing pressed, continue scanning
        if str(digit) == "*":
            print("Stop key pressed. Exiting")           
            break
        raw += str(digit)
        if len(raw) == 1:
            formatted = "00:0" + str(raw)
            lcd.clear()
            lcd.putstr(formatted)
        if len(raw) == 2:
            formatted = "00:" + str(raw)
            lcd.clear()
            lcd.putstr(formatted)
        if len(raw) == 3:
            formatted ="0" + str(raw)[0] + ":" + str(raw)[1:]
            lcd.clear()
            lcd.putstr(formatted)
        if len(raw) == 4:
            formatted =str(raw)[0:2] + ":" + str(raw)[2:]
            lcd.clear()
            lcd.putstr(formatted)
            break
        utime.sleep(0.3)
       
if len(str(raw)) == 4:
    minutes = int(str(raw)[0:2]) * 60
    seconds = int(str(raw)[2:])
if len(str(raw)) == 3:
    minutes = int(str(raw)[0:1]) * 60
    seconds = int(str(raw)[1:])
if len(str(raw)) == 2:
    minutes = 0
    seconds = int(str(raw))
if len(str(raw)) == 1:
    minutes = 0
    seconds = int(str(raw))
if len(str(raw)) == 0:
    minutes = 0
    seconds = 0
total = int(minutes) + int(seconds)
start = utime.ticks_ms()
percent = 12.5
duty = int(percent * 65535 / 100)
motor.duty_u16(duty)
old_time = ""
while True:
    end = utime.ticks_ms()
    elapsed = (end - start) / 1000
    remaining = int(total - elapsed)
        
    
    minutes = remaining // 60
    seconds = remaining % 60
    
    if (len(str(minutes)) == 1):
       minutes = "0" + str(minutes)
    if (len(str(seconds)) == 1):
        seconds = "0" + str(seconds)
    
    formatted = str(minutes) + ":" + str(seconds)
    
    
    if remaining <= 0:
        lcd.clear()
        lcd.putstr("00:00")
        motor.duty_u16(0)
        for i in range(3):
            buzzer.high() # turn on the buzzer on
            utime.sleep(0.5) # pause the program for 0.5 second
            buzzer.low() # turn off buzzer
            utime.sleep(0.5) # pause the program for 0.5 seconds
        break
    
    
    if not old_time == formatted:
        old_time = formatted
        lcd.clear()
        lcd.putstr(formatted)
        
    
        
        
   
    
   









    

