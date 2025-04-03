import pygame
import time
from gpiozero import Button
from signal import pause
import RPi.GPIO as GPIO
import threading

MOTOR_TIMEOUT = 10.0

def timer_callback():
    """ Timer callback to stop the motor after a time delay. """
    global motor_timer
    motor_moving = False
    stop_motor()

############ GLOBAL VARIABLES ############
play_music = False
motor_moving = False
motor_timer = threading.Timer(MOTOR_TIMEOUT, timer_callback)

in1 = 24
in2 = 23
en = 25
##########################################

# motor init (for some reason doesn't work if it's put in a separate func)
GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(en,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
p=GPIO.PWM(en,1000)
p.start(25)
print("\n")
print("The default speed & direction of motor is LOW & Forward.....")
print("r-run s-stop f-forward b-backward l-low m-medium h-high e-exit")
print("\n")   
#######

def init_mixer():
    """ Initialize mixer for music playback. """
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load("iliketomoveit.wav")
    print(f"Mixer initialized and music loaded")
    pygame.mixer.music.play()
    pygame.mixer.music.pause()
    print(f"Music played and paused. Ready for button press!")

def change_music_state():
    """ Play music if music is paused. Pause music if music is playing. """
    global play_music

    if pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()
        print("Music paused.")
        play_music = False
    else:
        pygame.mixer.music.unpause()
        print("Music playing.")
        play_music = True

def run_motor():
    global in1, in2
    print("run")
    GPIO.output(in1,GPIO.HIGH)
    GPIO.output(in2,GPIO.LOW)
    print("forward")

def stop_motor():
    global in1, in2
    print("stop")
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.LOW)

def change_motor_state():
    """ Stop motor if motor is moving, run motor if motor is stopped. """
    global motor_moving, motor_timer

    if motor_moving:
        motor_moving = False
        stop_motor()
    else:
        motor_moving = True
        if motor_timer.is_alive():
            motor_timer.cancel()
            motor_timer.join()
        
        motor_timer = threading.Timer(MOTOR_TIMEOUT, timer_callback)
        motor_timer.start()
        run_motor()
        

def button_pressed():
    """ Button callback. """
    print("Button pressed!")
    change_music_state()
    change_motor_state()
    
if __name__ == "__main__":
    init_mixer()

    button = Button(5, bounce_time=0.1)
    button.when_pressed = button_pressed

    try:
        pause()  # Keeps the script running
    except KeyboardInterrupt:
        print("\nExiting gracefully...")
        pygame.mixer.music.stop()
        stop_motor()
        motor_timer.cancel()
        motor_timer.join()
        GPIO.cleanup()
