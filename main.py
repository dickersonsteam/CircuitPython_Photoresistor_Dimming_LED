# Photoresistor Dimming an LED
# Target: Feather M0 Express
#
# This program reads the analog value of a voltage divider
# created with a photoresistor and 1K ohm resistor. The value is
# scaled to control the duty cycle of a PWM pin connected to an LED.
# As the light level hitting the photoresistor varies, the LED's
# brightness varies.

import analogio
import board
import pulseio

# scale(old_value, old_max, old_min, new_max, new_min)
#
# take a number in a range and fits it into a new range
# eg. the number 3 in the range 0-9 would scale to the number
#     33 in the range 0-99
#     scale(3, 9, 0, 99, 0) = 33
#
def scale(old_value, old_max, old_min, new_max, new_min):
    # If old_max and old_min are the same, there will be a divide
    # by zero error. You must account for this when calling this function.
    old_range = (old_max - old_min)  
    new_range = new_max - new_min
    return int((((old_value - old_min) * new_range) / old_range) + new_min)

# analog input from photoresistor
adc = analogio.AnalogIn(board.A1)

# record the current value of the adc
# take current value as the initial min and max reading
val = adc.value
min = val
max = val

# led is attached to this pin with a series resistor
pwm = pulseio.PWMOut(board.D9)


while True:
    # take a reading of the adc
    val = adc.value
 
    if val > max:
        max = val
        print("max =", max)
    if val < min:
        min = val
        print("min =", min)
    
    if max != min:
        # print("adc.value =", val)
        # print("min =", min)
        # print("max =", max)
        duty = scale(adc.value, max, min, 2**16-1, 0)
        # print("duty =", duty)
        
        if duty < 2**16 and duty >= 0:
            pwm.duty_cycle = duty
    