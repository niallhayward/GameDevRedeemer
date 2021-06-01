import pygame
import os
import sys
import math
import json
import data_handler as dh
import classes as cl


font_title = pygame.font.Font("Fixedsys.ttf", 120)
font_subtitle = pygame.font.Font("Fixedsys.ttf", 48)
font_text = pygame.font.Font("Fixedsys.ttf", 36)


def main():
    pygame.init()
    mainClock = pygame.time.Clock()
    pygame.mixer.init()
    pygame.mixer.music.load(os.path.join('Assets', "27 minute work.mp3"))
    settings_dict = dh.get_dict("settings")
    screen = cl.MainScreen(settings_dict)


    running = True
    while running:
        mainClock.tick(settings_dict["FPS"])





if __name__ == "__main__":
