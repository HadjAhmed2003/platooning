from PIL import ImageGrab
import sys
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame



def main():
    im = ImageGrab.grab()
    screen_fname = sys.argv[1]
    im.save(screen_fname, 'png') 
    pygame.init()
    print("{},{},{},{}".format(pygame.joystick.Joystick(0).get_axis(1), pygame.joystick.Joystick(0).get_axis(0), pygame.joystick.Joystick(0).get_axis(2), pygame.joystick.Joystick(0).get_axis(3)))


if __name__ == "__main__":
    main()
