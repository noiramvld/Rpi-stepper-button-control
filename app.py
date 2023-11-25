import RPi.GPIO as GPIO
import time

# Define GPIO pins for Motor 1 (ULN2003 Driver)
Motor1_A = 17  # GPIO 17
Motor1_B = 18  # GPIO 18
Motor1_C = 27  # GPIO 27
Motor1_D = 22  # GPIO 22

# Define GPIO pins for Motor 2 (ULN2003 Driver)
Motor2_A = 23  # GPIO 23
Motor2_B = 24  # GPIO 24
Motor2_C = 25  # GPIO 25
Motor2_D = 4   # GPIO 4

# Define GPIO pins for Buttons
Button1 = 5    # GPIO 5
Button2 = 6    # GPIO 6
Button3 = 12   # GPIO 12
Button4 = 13   # GPIO 13

# Motor sequence for half-stepping
seq = [ [1,0,0,0],
        [1,1,0,0],
        [0,1,0,0],
        [0,1,1,0],
        [0,0,1,0],
        [0,0,1,1],
        [0,0,0,1],
        [1,0,0,1] ]

def setup():
    GPIO.setmode(GPIO.BCM)
    # Motor 1 setup
    for pin in [Motor1_A, Motor1_B, Motor1_C, Motor1_D]:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, 0)
    # Motor 2 setup
    for pin in [Motor2_A, Motor2_B, Motor2_C, Motor2_D]:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, 0)
    # Buttons setup
    for button in [Button1, Button2, Button3, Button4]:
        GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def motor_step(motor, step):
    if motor == 1:
        pins = [Motor1_A, Motor1_B, Motor1_C, Motor1_D]
    elif motor == 2:
        pins = [Motor2_A, Motor2_B, Motor2_C, Motor2_D]
    
    for pin in range(4):
        GPIO.output(pins[pin], seq[step % len(seq)][pin])

def loop():
    step_count = len(seq)
    motor1_step = 0
    motor2_step = 0

    while True:
        if not GPIO.input(Button1):  # Button 1 pressed
            motor1_step += 1
            motor_step(1, motor1_step)
        elif not GPIO.input(Button2):  # Button 2 pressed
            motor1_step -= 1
            motor_step(1, motor1_step)
        elif not GPIO.input(Button3):  # Button 3 pressed
            motor2_step += 1
            motor_step(2, motor2_step)
        elif not GPIO.input(Button4):  # Button 4 pressed
            motor2_step -= 1
            motor_step(2, motor2_step)

        time.sleep(0.001)  # Adjust this for speed control

def destroy():
    GPIO.cleanup()

if __name__ == '__main__':
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
