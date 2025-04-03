import pygame
import time
from signal import pause
import RPi.GPIO as GPIO
import threading
from gpiozero import Button

############ GLOBAL VARIABLES ############
playing = False

in1 = 24
in2 = 23
en = 25
button = 5
##########################################
GPIO.setmode(GPIO.BCM)
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# motor init (for some reason doesn't work if it's put in a separate func)
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

def play_music():
    pygame.mixer.music.play()
    print("Music playing.")

def move_motor():
    global in1, in2
    p.ChangeDutyCycle(25)
    for i in range (4):
        print("run")
        print("forward")
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)
        
        time.sleep(1)

        print("backward")
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.HIGH)

        time.sleep(1)

    print("forward")
    GPIO.output(in1,GPIO.HIGH)
    GPIO.output(in2,GPIO.LOW)
    p.ChangeDutyCycle(50)

    time.sleep(4)

    print("stop")
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.LOW)

def stop_motor():
    global in1, in2
    print("stop")
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.LOW)

# def button_pressed():
#     """ Button callback. """
#     global playing

#     print("Button pressed!")
#     print(f"playing: {playing}")

#     if playing:
#         print("Button pressed, but function is currently running. Ignoring.")
#     else:
#         print("Button pressed, executing function...")
#         playing = True
#         play_music()
#         move_motor()
#         while pygame.mixer.music.get_busy():

            
#         playing = False
    
if __name__ == "__main__":
    init_mixer()

    # button = Button(5, bounce_time=0.1)
    # button.when_pressed = button_pressed

    while True: # Run forever
        if GPIO.input(button) == GPIO.HIGH:
            print("Button was pushed!")
            music_thread = threading.Thread(target=play_music)
            motor_thread = threading.Thread(target=move_motor)
            music_thread.start()
            motor_thread.start()
            time.sleep(13)
            music_thread.join()
            motor_thread.join()

    try:
        pause()  # Keeps the script running
    except KeyboardInterrupt:
        print("\nExiting gracefully...")
        music_thread.join()
        motor_thread.join()
        pygame.mixer.music.stop()
        stop_motor()
        GPIO.cleanup()
