import sys
import pygame
import background_classes
import data_handler
import enemy_classes
import player_classes


class Game:
    def __init__(self, running, screen, level, stage, fps):
        self.running = running
        self.level = level
        self.stage = stage
        self.screen = screen
        self.fps = fps
        self.enemy_pods_dict = data_handler.get_dict("enemies")
        self.current_background = background_classes.Background(screen.screen, fps,
                                                                *data_handler.get_dict("levels")[str(self.level)][
                                                                    "backgrounds"])
        self.background_handler = background_classes.BackgroundHandler([self.current_background], [])
        self.enemy_pods = [enemy_classes.EnemyPod(self.fps,
                                        [self.fps, *self.enemy_pods_dict[str(self.level)][str(self.stage)]["Enemy"]],
                                        self.enemy_pods_dict[str(self.level)][str(self.stage)]["Delay"],
                                        self.enemy_pods_dict[str(self.level)][str(self.stage)]["Size"],
                                        self.enemy_pods_dict[str(self.level)][str(self.stage)]["Spawn Type"])]

        self.player = player_classes.Player(fps, "playership", 0, [80, 80],
                                 [screen.resolution[0] / 2, screen.resolution[1] * (9 / 10)], [6, 6], 100, 3)
        self.timer = 360

    def is_next_stage(self):
        if self.enemy_pods[self.stage].size == 0:
            if self.timer <= 0:
                self.stage += 1
                self.enemy_pods.append(enemy_classes.EnemyPod(self.fps,
                                                    [self.fps,
                                                     *self.enemy_pods_dict[str(self.level)][str(self.stage)]["Enemy"]],
                                                    self.enemy_pods_dict[str(self.level)][str(self.stage)]["Delay"],
                                                    self.enemy_pods_dict[str(self.level)][str(self.stage)]["Size"],
                                                    self.enemy_pods_dict[str(self.level)][str(self.stage)][
                                                        "Spawn Type"]))
                self.timer = 360
            self.timer -= 1

    def start(self, clock):
        while self.running:
            clock.tick(self.fps)
            self.screen.full_game_screen_update(self.player, self.enemy_pods, self.background_handler)
            # event handling, gets all event from the event queue
            click = False
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
            self.is_next_stage()
            pygame.display.update()
