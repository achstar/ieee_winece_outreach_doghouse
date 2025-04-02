import pygame
import time

pygame.mixer.init()
pygame.mixer.music.load("iliketomoveit.wav")  
pygame.mixer.music.play()

while True:
    cmd = input("Enter 'p' to pause/play, 'q' to quit: ").strip().lower()
    if cmd == "p":
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            print("Paused")
        else:
            pygame.mixer.music.unpause()
            print("Playing")
    elif cmd == "q":
        pygame.mixer.music.stop()
        break