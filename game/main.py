import pygame
import os
import sys
import math
import json
import data_handler as dh

def main():
    pygame.init()
    mainClock = pygame.time.Clock()
    pygame.mixer.init()
    pygame.mixer.music.load(os.path.join('Assets', "27 minute work.mp3"))

