import sys
import pygame
import background_classes
import data_handler
import game_classes
import screen_classes


pygame.init()
font_title = pygame.font.Font("Fixedsys.ttf", 120)
font_subtitle = pygame.font.Font("Fixedsys.ttf", 48)
font_text = pygame.font.Font("Fixedsys.ttf", 36)


def main():
    main_clock = pygame.time.Clock()
    pygame.mixer.init()
    pygame.mixer.music.load(data_handler.get_music("level1", "mp3"))
    settings_dict = data_handler.get_dict("settings")
    screen = screen_classes.Screen(settings_dict)
    screen.start()
    background_handler = background_classes.BackgroundHandler(
        [background_classes.Background(screen.screen, settings_dict["FPS"], "space background", [0, 0], [0, 0.5],
                        [screen.resolution[0], screen.resolution[1] * 2])], [])
    pygame.mixer.music.set_volume(settings_dict["MusicVolume"])
    pygame.mixer.music.play()
    click = False
    running = True
    while running:
        main_clock.tick(settings_dict["FPS"])
        screen.draw_screen_menu(background_handler)
        screen.draw_text("REDEEMER", font_title, (160, 0, 0), screen.resolution[0] // 2, 100, True)
        button_play_game = screen.draw_text("PLAY", font_subtitle, (160, 0, 0), 50, 300, False)
        my, mx = pygame.mouse.get_pos()
        if button_play_game.collidepoint(my, mx):
            if click:
                game = game_classes.Game(True, screen, 0, 0, settings_dict["FPS"])
                game.start(main_clock)
        click = False
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
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
