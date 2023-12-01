import pygame

import background_classes as bac


class Screen:
    def __init__(self, settings_dict):
        self.resolution = tuple(settings_dict["Resolution"])
        self.fullscreen = settings_dict["FullScreen"]
        self.borderless = settings_dict["Borderless"]
        self.fps = settings_dict["FPS"]
        self.screen = None
        self.explosions = []

    def start(self):
        if self.borderless:
            self.screen = pygame.display.set_mode(self.resolution, pygame.NOFRAME)
        else:
            self.screen = pygame.display.set_mode(self.resolution)

    def draw_screen_menu(self, background_handler):
        for background in background_handler.background_list:
            background.scroll_background()
            self.screen.blit(background.image, background.coordinates)

    def draw_screen_game(self, player, enemy_pods, background_handler):
        for background in background_handler.background_list:
            background.scroll_background()
            self.screen.blit(background.image, background.coordinates)
        self.screen.blit(player.image, player.coordinates)
        for projectile in player.projectiles:
            self.screen.blit(projectile.image, projectile.coordinates)
        for pod in enemy_pods:
            for enemy in pod.pod:
                # pygame.draw.rect(self.screen, (255, 0, 0), pygame.Rect(enemy.coordinates, enemy.size))  # DEBUGGER
                self.screen.blit(enemy.image, enemy.coordinates)
            for projectile in pod.projectiles:
                self.screen.blit(projectile.image, projectile.coordinates)
        for explosion in self.explosions:
            explosion.explode()
            self.screen.blit(explosion.image, explosion.coordinates)
            if explosion.stage == 11:
                self.explosions.remove(explosion)
        pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(10, 10, 140, 40))
        pygame.draw.rect(self.screen, (255, 0, 0), pygame.Rect(14, 14, (132 * (player.health / 100)), 32))

    def draw_text(self, text, font, colour, x, y, centred):
        textobj = font.render(text, 1, colour)
        textrect = textobj.get_rect()
        if centred:
            x -= textrect.width // 2
        textrect.topleft = (x, y)
        self.screen.blit(textobj, textrect)
        return textrect

    def update(self, player, enemy_pods):
        player.update(pygame.key.get_pressed())
        for pod in enemy_pods:
            pod.spawn()
            pod.move_all()
            pod.update_projectiles()

    def handle_events(self, player, enemy_pods):
        for pod in enemy_pods:
            for projectile in pod.projectiles:
                mark_to_delete = False
                if player.get_hitbox().colliderect(projectile.get_hitbox()):
                    player.health -= 1
                    mark_to_delete = True
                if mark_to_delete:
                    pod.projectiles.remove(projectile)
        for projectile in player.projectiles:
            mark_to_delete = False
            for pod in enemy_pods:
                for enemy in pod.pod:
                    if enemy.get_hitbox().colliderect(projectile.get_hitbox()):
                        enemy.health -= 1
                        mark_to_delete = True
                        if enemy.health == 0:
                            self.explosions.append(bac.Explosion(self.screen, enemy))
                            pod.pod.remove(enemy)
            if mark_to_delete:
                player.projectiles.remove(projectile)

    def full_game_screen_update(self, player, enemy_pods, background_handler):
        self.draw_screen_game(player, enemy_pods, background_handler)
        self.update(player, enemy_pods)
        self.handle_events(player, enemy_pods)
