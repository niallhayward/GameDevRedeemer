import pygame
import os
import sys
import math
import json
import data_handler as dh
import classes as cl

pygame.init()
font_title = pygame.font.Font("Fixedsys.ttf", 120)
font_subtitle = pygame.font.Font("Fixedsys.ttf", 48)
font_text = pygame.font.Font("Fixedsys.ttf", 36)


def main():
    main_clock = pygame.time.Clock()
    pygame.mixer.init()
    pygame.mixer.music.load(dh.get_music("level1", "mp3"))
    settings_dict = dh.get_dict("settings")
    screen = cl.MainScreen(settings_dict)
    screen.start()
    background_handler = cl.BackgroundHandler(
        [cl.Background(screen.screen, settings_dict["FPS"], "space background", 0, 0, 0, 0.5, screen.resolution, 1)], [])
    pygame.mixer.music.set_volume(settings_dict["MusicVolume"])
    pygame.mixer.music.play()
    click = False
    running = True
    while running:
        main_clock.tick(settings_dict["FPS"])
        background_handler.move_backgrounds()
        screen.draw_screen_menu(background_handler)
        screen.draw_text("REDEEMER", font_title, (160, 0, 0), screen.resolution[0] // 2, 100, True)
        button_play_game = screen.draw_text("PLAY", font_subtitle, (160, 0, 0), 50, 300, False)
        my, mx = pygame.mouse.get_pos()
        if button_play_game.collidepoint(my, mx):
            if click:
                print("clicked")
        click = False
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        pygame.display.update()
if __name__ == "__main__":
    main()
